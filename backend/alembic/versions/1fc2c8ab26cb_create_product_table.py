"""create product table

Revision ID: 1fc2c8ab26cb
Revises: e161903d4bae
Create Date: 2023-08-30 11:10:45.717283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1fc2c8ab26cb'
down_revision: Union[str, None] = 'e161903d4bae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('description', sa.String(length=30), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'categories', ['description'])


def downgrade() -> None:
    op.drop_constraint(None, 'categories', type_='unique')
    op.drop_table('products')
