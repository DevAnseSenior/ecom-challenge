"""create table sales

Revision ID: 368638a176a8
Revises: f98ea4f701b1
Create Date: 2023-09-01 00:28:18.089559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '368638a176a8'
down_revision: Union[str, None] = 'f98ea4f701b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_id'), 'sales', ['id'], unique=False)
    op.drop_constraint('products_owner_id_key', 'products', type_='unique')
    op.drop_constraint('products_owner_id_fkey', 'products', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('products_owner_id_fkey', 'products', 'users', ['owner_id'], ['id'])
    op.create_unique_constraint('products_owner_id_key', 'products', ['owner_id'])
    op.drop_index(op.f('ix_sales_id'), table_name='sales')
    op.drop_table('sales')
    # ### end Alembic commands ###
