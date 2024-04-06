"""initial migration

Revision ID:9db626d0eb84
Revises:
Create Date:2022-09-26 14:54:07.075092

"""
import sqlalchemy as sa
from alembic import op

revision: str = "9db626d0eb84"
down_revision: str | tuple[str, ...] | None = None
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("pk_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint("pk_id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("user")
