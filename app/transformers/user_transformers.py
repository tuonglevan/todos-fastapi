from app.models import User
from app.schemas.user import UserResponseDetail

def transform_to_user_response(user: User) -> UserResponseDetail:
    return UserResponseDetail(
        id=user.id,
        company_name=user.company.name if user.company else None,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at
    )