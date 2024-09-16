"""create user table

Revision ID: 6dffa6dbc6f8
Revises: 
Create Date: 2024-09-16 12:39:45.944253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dffa6dbc6f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(128), nullable=False),
        sa.Column('password', sa.String(128), nullable=False),
        sa.Column('email', sa.String(128), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('user')
