from typing import Sequence
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from app.models import User
from app.models.user import get_password_hash
from app.schemas.user import UserCreate, UserUpdate
from .base_crud_service import BaseCRUDService

class UserService(BaseCRUDService):
    def __init__(self, async_session: AsyncSession = None, sync_session: Session = None):
        super().__init__(async_session, sync_session)

    async def get_users(self) -> Sequence[User]:
        result = await self.async_session.execute(
            select(User)
            .options(joinedload(User.company, innerjoin=True))
            .order_by(desc(User.created_at))
        )
        return result.scalars().all()

    async def fetch_user_by_username(self, username: str) -> User:
        result = await self.async_session.scalars(select(User).filter(cast(User.username == username, Boolean)))
        return result.first()

    async def get_user_by_id(self, user_id: UUID) -> User:
        result = await self.async_session.execute(
            select(User)
            .options(joinedload(User.company, innerjoin=True))
            .filter(cast(User.id == user_id, Boolean))
        )
        return result.scalar_one_or_none()

    def create_user(self, user_create: UserCreate) -> User:
        # Hash the plain-text password
        hashed_password = get_password_hash(user_create.password)
        # Get the dictionary representation of the user and update the password
        user_dict = user_create.model_dump()
        user_dict['hashed_password'] = hashed_password
        del user_dict['password'] # Ensure the plain-text password is not saved

        # Create the User instance with the updated dictionary
        db_user = User(**user_dict)
        self.sync_session.add(db_user)
        self.sync_session.commit()
        self.sync_session.refresh(db_user)

        return db_user

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> User | None:
        result = await self.async_session.execute(
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
        self.async_session.add(user_info)
        await self.async_session.commit()
        await self.async_session.refresh(user_info)

        return user_info

    async def delete_user(self, user_id: UUID) -> bool:
        return await self.delete_by_id(User, user_id)