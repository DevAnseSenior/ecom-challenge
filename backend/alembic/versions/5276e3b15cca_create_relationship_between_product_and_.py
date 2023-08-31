"""create relationship between product and category

Revision ID: 5276e3b15cca
Revises: b79d7370e101
Create Date: 2023-08-30 20:56:01.118372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5276e3b15cca'
down_revision: Union[str, None] = 'b79d7370e101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products',
                  sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'categories', ['category_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'category_id')
