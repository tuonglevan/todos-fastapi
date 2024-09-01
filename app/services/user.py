from typing import Sequence
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from app.models import User
from app.models.user import get_password_hash
from app.schemas.user import UserCreate, UserUpdate
from .crud_helpers import delete_record

async def get_users(async_session: AsyncSession) -> Sequence[User]:
    result = await async_session.execute(
        select(User)
        .options(joinedload(User.company, innerjoin=True))
        .order_by(desc(User.created_at))
    )
    return result.scalars().all()

async def fetch_user_by_username(async_session: AsyncSession, username: str) -> User:
    result = await async_session.scalars(select(User).filter(cast(User.username == username, Boolean)))
    return result.first()

async def get_user_by_id(async_session: AsyncSession, user_id: UUID) -> User:
    result = await async_session.execute(
        select(User)
        .options(joinedload(User.company, innerjoin=True))
        .filter(cast(User.id == user_id, Boolean))
    )
    return result.scalar_one_or_none()

def create_user(sync_session: Session, user: UserCreate) -> User:
    # Hash the plain-text password
    hashed_password = get_password_hash(user.password)
    # Get the dictionary representation of the user and update the password
    user_dict = user.model_dump()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password'] # Ensure the plain-text password is not saved

    # Create the User instance with the updated dictionary
    db_user = User(**user_dict)
    sync_session.add(db_user)
    sync_session.commit()
    sync_session.refresh(db_user)

    return db_user

async def update_user(async_session: AsyncSession, user_id: UUID, user_update: UserUpdate) -> User | None:
    result = await async_session.execute(
        select(User)
        .options(joinedload(User.company, innerjoin=True))
        .where(cast(User.id == user_id, Boolean))
    )
    user_info = result.scalar_one_or_none()
    if not user_info:
        return None

    for attr, value in user_update.model_dump(exclude_unset=True).items():
        if attr == 'password':
            value = get_password_hash(value)
            attr = 'hashed_password'
        setattr(user_info, attr, value)
    async_session.add(user_info)
    await async_session.commit()
    await async_session.refresh(user_info)

    return user_info

async def delete_user(async_session: AsyncSession, user_id: UUID) -> bool:
    return await delete_record(async_session, User, user_id)