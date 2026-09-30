"""add content column to post table

Revision ID: 77a40f0c9f31
Revises: 1df172a054e1
Create Date: 2026-09-22 20:30:11.938891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77a40f0c9f31'
down_revision: Union[str, Sequence[str], None] = '1df172a054e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Posts', 'content')
    pass
