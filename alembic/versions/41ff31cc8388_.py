"""empty message

Revision ID: 41ff31cc8388
Revises:
Create Date: 2021-10-26 12:06:47.917788

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "41ff31cc8388"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "installation_requests",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("budget", sa.DECIMAL(), nullable=False),
        sa.Column("equipment_brand", sa.String(), nullable=True),
        sa.Column("equipment_model", sa.String(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("equipment_type", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("NEW", "PENDING", "CLOSED", "CANCELED", name="requestStatus"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass
