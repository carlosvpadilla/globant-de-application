"""Create initial schema

Revision ID: a2c29e62148c
Revises: 
Create Date: 2023-08-01 21:30:44.299783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c29e62148c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('department', sa.String(1000), nullable=False)
    )

    op.create_table(
        "jobs",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job', sa.String(1000), nullable=False)
    )

    op.create_table(
        "hired_employees",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(1000), nullable=False),
        sa.Column('datetime', sa.DateTime, nullable=False),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('job_id', sa.Integer, sa.ForeignKey('jobs.id'), nullable=False)
    )


def downgrade() -> None:
    pass
