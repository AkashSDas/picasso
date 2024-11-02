"""initial

Revision ID: 6f73ef3ce735
Revises:
Create Date: 2024-11-01 04:15:25.754384+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f73ef3ce735"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_user_id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_banned", sa.Boolean(), nullable=False),
        sa.Column("profile_pic_url", sa.String(length=255), nullable=False),
        sa.Column("profile_pic_id", sa.String(length=32), nullable=True),
        sa.Column("upload_consumed", sa.Integer(), nullable=False),
        sa.Column(
            "upload_consumed_updated_at", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_public_user_id"), "users", ["public_user_id"], unique=True
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "magic_links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("unhashed_token", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_magic_links_id"), "magic_links", ["id"], unique=False)
    op.create_index(
        op.f("ix_magic_links_unhashed_token"),
        "magic_links",
        ["unhashed_token"],
        unique=False,
    )
    op.create_index(
        op.f("ix_magic_links_user_id"), "magic_links", ["user_id"], unique=True
    )
    op.create_table(
        "style_filters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_filter_id", sa.UUID(), nullable=False),
        sa.Column("base_img_url", sa.String(length=2048), nullable=False),
        sa.Column("blur_img_url", sa.String(length=2048), nullable=False),
        sa.Column("small_img_url", sa.String(length=2048), nullable=False),
        sa.Column("img_id", sa.String(length=32), nullable=True),
        sa.Column("is_official", sa.Boolean(), nullable=False),
        sa.Column("is_banned", sa.Boolean(), nullable=False),
        sa.Column("report_count", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_style_filters_author_id"), "style_filters", ["author_id"], unique=False
    )
    op.create_index(op.f("ix_style_filters_id"), "style_filters", ["id"], unique=False)
    op.create_index(
        op.f("ix_style_filters_public_filter_id"),
        "style_filters",
        ["public_filter_id"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_style_filters_public_filter_id"), table_name="style_filters")
    op.drop_index(op.f("ix_style_filters_id"), table_name="style_filters")
    op.drop_index(op.f("ix_style_filters_author_id"), table_name="style_filters")
    op.drop_table("style_filters")
    op.drop_index(op.f("ix_magic_links_user_id"), table_name="magic_links")
    op.drop_index(op.f("ix_magic_links_unhashed_token"), table_name="magic_links")
    op.drop_index(op.f("ix_magic_links_id"), table_name="magic_links")
    op.drop_table("magic_links")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_public_user_id"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###