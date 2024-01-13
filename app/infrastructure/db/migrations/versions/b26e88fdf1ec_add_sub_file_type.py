"""add sub file type

Revision ID: b26e88fdf1ec
Revises: 086f55fe8c2d
Create Date: 2024-01-14 03:00:14.726954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b26e88fdf1ec'
down_revision: Union[str, None] = '086f55fe8c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


sub_type_enum = sa.Enum('doc_text', 'doc_image', 'doc_video', 'doc_audio', name='subfiletype')


def upgrade() -> None:
    sub_type_enum.create(op.get_bind())
    op.add_column('files', sa.Column('sub_type', sub_type_enum, nullable=True))


def downgrade() -> None:
    op.drop_column('files', 'sub_type')
    sub_type_enum.drop(op.get_bind())