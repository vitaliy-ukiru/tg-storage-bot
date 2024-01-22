"""add user locales

Revision ID: bc19050003af
Revises: 7383c62bf48f
Create Date: 2024-01-23 02:14:11.371261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc19050003af'
down_revision: Union[str, None] = '7383c62bf48f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('locale', sa.String(), server_default='en', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'locale')
    # ### end Alembic commands ###