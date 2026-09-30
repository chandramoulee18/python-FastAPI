"""add last few columns  to post table

Revision ID: 04821751ca26
Revises: 9518b0e8eaf3
Create Date: 2026-09-22 22:25:53.197550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04821751ca26'
down_revision: Union[str, Sequence[str], None] = '9518b0e8eaf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('Posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    pass
