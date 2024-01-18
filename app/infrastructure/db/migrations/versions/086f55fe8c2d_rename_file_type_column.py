"""rename file type column

Revision ID: 086f55fe8c2d
Revises: aaddf08b3d7b
Create Date: 2024-01-14 02:55:58.440173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '086f55fe8c2d'
down_revision: Union[str, None] = 'aaddf08b3d7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('files', 'type_id', new_column_name="file_type")
    op.execute("""ALTER TYPE filetype rename to filecategory""")


def downgrade() -> None:
    op.alter_column('files', 'file_type', new_column_name="type_id")
    op.execute("""ALTER TYPE filecategory rename to filetype""")
