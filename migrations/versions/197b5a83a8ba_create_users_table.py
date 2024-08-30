"""Create users table

Revision ID: 197b5a83a8ba
Revises: 
Create Date: 2024-08-28 17:32:59.746583

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from app.core.config import get_config
from app.models.user import get_password_hash
from app.utils.time_utils import get_current_utc_datetime

# revision identifiers, used by Alembic.
revision: str = '197b5a83a8ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

USERS_TABLE = "users"
DEFAULT_IS_ACTIVE = True
DEFAULT_IS_ADMIN = False

def upgrade() -> None:
    user_table = op.create_table(
        USERS_TABLE,
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=DEFAULT_IS_ACTIVE),
        sa.Column("is_admin", sa.Boolean, default=DEFAULT_IS_ADMIN),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )
    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "fastapi_todo@sample.com",
            "username": "admin",
            "first_name": "FastApi",
            "last_name": "Admin",
            "hashed_password": get_password_hash(get_config().DEFAULT_PASSWORD_ADMIN),
            "is_active": True,
            "is_admin": True,
            "created_at": get_current_utc_datetime(),
            "updated_at": get_current_utc_datetime()
        }
    ])

def downgrade() -> None:
    op.drop_table(USERS_TABLE)