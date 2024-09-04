from typing import Sequence

from app.models import User
from app.schemas.company import CompanyInfo
from app.schemas.paginate import PaginatedResponse
from app.schemas.user import UserResponseDetail

# Define a type alias for PaginatedResponse of TaskResponseDetail
UsersPaginatedResponse = PaginatedResponse[UserResponseDetail]

def transform_to_user_response(user: User) -> UserResponseDetail:
    return UserResponseDetail(
        id=user.id,
        company_info=CompanyInfo(
            company_id=user.company_id,
            name=user.company.name,
            status="Active" if user.company.mode else "Inactive",
        ),
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at
    )

def generate_tasks_paginated_response(users: Sequence[User], total: int, skip: int, limit: int) -> UsersPaginatedResponse:
    return UsersPaginatedResponse(
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        items=[transform_to_user_response(user) for user in users]
    )