"""add marker column

Revision ID: b149175aeb2b
Revises: bc19050003af
Create Date: 2024-02-07 21:26:23.660356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b149175aeb2b'
down_revision: Union[str, None] = 'bc19050003af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('marker', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'marker')
    # ### end Alembic commands ###