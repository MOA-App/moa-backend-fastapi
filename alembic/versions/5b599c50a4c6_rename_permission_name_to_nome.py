"""rename permission name to nome

Revision ID: 5b599c50a4c6
Revises: d052146fca64
Create Date: 2026-03-11 11:03:21.977862

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5b599c50a4c6'
down_revision: Union[str, Sequence[str], None] = 'd052146fca64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "permissions",
        "name",
        new_column_name="nome"
    )


def downgrade():
    op.alter_column(
        "permissions",
        "nome",
        new_column_name="name"
    )
