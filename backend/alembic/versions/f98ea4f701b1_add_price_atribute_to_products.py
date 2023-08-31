"""add price atribute to products

Revision ID: f98ea4f701b1
Revises: 855bc9466b01
Create Date: 2023-08-31 00:01:19.809702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f98ea4f701b1'
down_revision: Union[str, None] = '855bc9466b01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('price', sa.Float(), nullable=False))


def downgrade() -> None:
    op.drop_column('products', 'price')
