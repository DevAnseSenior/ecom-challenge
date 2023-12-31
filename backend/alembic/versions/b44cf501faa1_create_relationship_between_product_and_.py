"""create relationship between product and user

Revision ID: b44cf501faa1
Revises: 5276e3b15cca
Create Date: 2023-08-30 21:05:36.848381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b44cf501faa1'
down_revision: Union[str, None] = '5276e3b15cca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'users', ['owner_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'owner_id')
