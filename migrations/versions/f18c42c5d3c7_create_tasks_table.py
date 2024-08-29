"""Create tasks table

Revision ID: f18c42c5d3c7
Revises: 197b5a83a8ba
Create Date: 2024-08-28 18:05:12.392363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f18c42c5d3c7'
down_revision: Union[str, None] = '197b5a83a8ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

STATUS_ENUM = 'statusenum'
PRIORITY_ENUM = 'priorityenum'
TASKS_TABLE = 'tasks'


def upgrade() -> None:
    op.create_table(
        TASKS_TABLE,
        sa.Column('id', sa.UUID, primary_key=True, index=True),
        sa.Column('user_id', sa.UUID, nullable=False, index=True),
        sa.Column('summary', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('TODO', 'IN_PROGRESS', 'DONE', name=STATUS_ENUM), nullable=False,
                  default='TODO'),
        sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', name=PRIORITY_ENUM), nullable=False,
                  default='MEDIUM'),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )
    # Create foreign key constraint
    op.create_foreign_key('fk_tasks_user_id', 'tasks', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_tasks_user_id', TASKS_TABLE, type_='foreignkey')
    # Drop the tasks table
    op.drop_table(TASKS_TABLE)
    # Drop the StatusEnum and PriorityEnum types
    op.execute(f'DROP TYPE {STATUS_ENUM}')
    op.execute(f'DROP TYPE {PRIORITY_ENUM}')