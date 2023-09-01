"""create sales table and improve owner id in products

Revision ID: 261422cc2b99
Revises: f98ea4f701b1
Create Date: 2023-08-31 21:11:11.407615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '261422cc2b99'
down_revision: Union[str, None] = 'f98ea4f701b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'products', ['owner_id'])
    op.create_table('sales',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=True),
                    sa.Column('seller_id', sa.Integer(), nullable=True),
                    sa.Column('customer_id', sa.Integer(), nullable=True),
                    sa.Column('quantity', sa.Integer(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['seller_id'], ['products.owner_id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_sales_id'), 'sales', ['id'], unique=False)


def downgrade() -> None:
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_index(op.f('ix_sales_id'), table_name='sales')
    op.drop_table('sales')
