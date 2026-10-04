"""set created_at server default

Revision ID: c07f3e9d6a21
Revises: a4f356db1714
Create Date: 2026-10-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c07f3e9d6a21'
down_revision: Union[str, Sequence[str], None] = 'a4f356db1714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('posts') as batch_op:
        batch_op.alter_column(
            'created_at',
            existing_type=sa.DateTime(),
            existing_nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP'),
        )


def downgrade() -> None:
    with op.batch_alter_table('posts') as batch_op:
        batch_op.alter_column(
            'created_at',
            existing_type=sa.DateTime(),
            existing_nullable=False,
            server_default=None,
        )