"""create extension vector

Revision ID: ba5e378ae398
Revises: 6dffa6dbc6f8
Create Date: 2024-09-17 11:54:29.140939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba5e378ae398'
down_revision: Union[str, None] = '6dffa6dbc6f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")  
