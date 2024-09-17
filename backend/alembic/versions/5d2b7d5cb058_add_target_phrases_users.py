"""add target phrases users

Revision ID: 5d2b7d5cb058
Revises: f0ec5abf8f19
Create Date: 2024-09-17 12:42:32.119698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d2b7d5cb058'
down_revision: Union[str, None] = 'f0ec5abf8f19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('signup_phrases_target', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'signup_phrases_target')
