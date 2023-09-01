"""turn app and owner id mandatory

Revision ID: 855bc9466b01
Revises: b44cf501faa1
Create Date: 2023-08-30 21:21:24.903418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '855bc9466b01'
down_revision: Union[str, None] = 'b44cf501faa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('products', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('products', 'owner_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)


def downgrade() -> None:
    op.alter_column('products', 'owner_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.alter_column('products', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
