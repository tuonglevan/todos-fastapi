"""Create companies table

Revision ID: d707de36f623
Revises: f18c42c5d3c7
Create Date: 2024-08-28 18:38:51.519827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd707de36f623'
down_revision: Union[str, None] = 'f18c42c5d3c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

USERS_TABLE = "users"
COMPANIES_TABLE = "companies"

def upgrade() -> None:
    op.create_table(
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

def downgrade() -> None:
    # Drop foreign key constraint for company_id in users table
    op.drop_constraint('fk_users_company_id', USERS_TABLE, type_='foreignkey')

    # Drop company_id column from users table
    op.drop_column(USERS_TABLE, 'company_id')

    # Drop companies table
    op.drop_table(COMPANIES_TABLE)
