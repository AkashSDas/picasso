"""increase img_id size in style_filter table

Revision ID: 2cb4ce5113c7
Revises: 278dff1e363f
Create Date: 2024-11-02 06:30:55.354417+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2cb4ce5113c7"
down_revision: Union[str, None] = "278dff1e363f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "style_filters",
        "img_id",
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "style_filters",
        "img_id",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=32),
        existing_nullable=True,
    )
    # ### end Alembic commands ###