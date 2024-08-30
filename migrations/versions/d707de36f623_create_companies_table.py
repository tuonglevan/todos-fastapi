"""Create companies table

Revision ID: d707de36f623
Revises: f18c42c5d3c7
Create Date: 2024-08-28 18:38:51.519827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.utils.time_utils import get_current_utc_datetime

# revision identifiers, used by Alembic.
revision: str = 'd707de36f623'
down_revision: Union[str, None] = 'f18c42c5d3c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

USERS_TABLE = "users"
COMPANIES_TABLE = "companies"

def upgrade() -> None:
    company_table = op.create_table(
        COMPANIES_TABLE,
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("mode", sa.String(length=50), nullable=False),
        sa.Column("rating", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )
    # Add company_id column to users table
    op.add_column(USERS_TABLE, sa.Column('company_id', sa.UUID, nullable=True))

    # Create foreign key constraint for company_id in users table
    op.create_foreign_key('fk_users_company_id', USERS_TABLE, COMPANIES_TABLE, ['company_id'], ['id'])

    # Data seed for first company
    company_id = "123e4567-e89b-12d3-a456-426655440000"
    op.bulk_insert(company_table, [
        {
            "id": company_id,
            "name": "FastApi",
            "description": "FastApi is a framework for building fast APIs",
            "mode": "remote",
            "rating": 4.5,
            "created_at": get_current_utc_datetime(),
            "updated_at": get_current_utc_datetime()
        }
    ])
    # Update existing records in users table to set company_uid
    op.execute(
        f"UPDATE {USERS_TABLE} SET company_id = '{company_id}' WHERE company_id IS NULL"
    )

def downgrade() -> None:
    company_id = "123e4567-e89b-12d3-a456-426655440000"
    # Update existing records in users table to remove company_uid
    op.execute(
        f"UPDATE {USERS_TABLE} SET company_id = NULL WHERE company_id = '{company_id}'"
    )
    # Drop foreign key constraint for company_id in users table
    op.drop_constraint('fk_users_company_id', USERS_TABLE, type_='foreignkey')

    # Drop company_id column from users table
    op.drop_column(USERS_TABLE, 'company_id')

    # Drop companies table
    op.drop_table(COMPANIES_TABLE)
