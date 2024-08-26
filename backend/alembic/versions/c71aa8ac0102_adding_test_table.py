"""adding test table

Revision ID: c71aa8ac0102
Revises: 
Create Date: 2024-08-25 18:46:48.328077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c71aa8ac0102'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'test_data',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('value', sa.String(255), nullable=True),
    )
    pass


def downgrade() -> None:
    op.drop_table('test_data')
    pass