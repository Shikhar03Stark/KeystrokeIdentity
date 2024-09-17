"""signup status alter table

Revision ID: f0ec5abf8f19
Revises: ba5e378ae398
Create Date: 2024-09-17 12:26:49.983301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0ec5abf8f19'
down_revision: Union[str, None] = 'ba5e378ae398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add optional columns singup_status and signup_phrases_completed
    op.add_column('users', sa.Column('signup_status', sa.String(128), nullable=True))
    op.add_column('users', sa.Column('signup_phrases_completed', sa.Integer, nullable=True))


def downgrade() -> None:
    # drop columns signup_status and signup_phrases_completed
    op.drop_column('users', 'signup_status')
    op.drop_column('users', 'signup_phrases_completed')
