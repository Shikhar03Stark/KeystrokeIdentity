"""create embeddings table

Revision ID: 9714783a2c92
Revises: 5d2b7d5cb058
Create Date: 2024-09-17 13:22:03.547771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9714783a2c92'
down_revision: Union[str, None] = '5d2b7d5cb058'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS embeddings (
            id SERIAL PRIMARY KEY,
            embedding vector(64) NOT NULL,
            user_id INTEGER,
            purpose VARCHAR(32),
            CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id)
        )"""
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS embeddings")
