"""add foreign key to post table

Revision ID: 9518b0e8eaf3
Revises: 6f361c769ddb
Create Date: 2026-09-22 20:55:40.699273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9518b0e8eaf3'
down_revision: Union[str, Sequence[str], None] = '6f361c769ddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='Posts', referent_table='Users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='Posts')
    op.drop_column('Posts', 'owner_id')
    pass
