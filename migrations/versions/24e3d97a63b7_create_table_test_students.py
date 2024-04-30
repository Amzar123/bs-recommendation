"""create table test students

Revision ID: 24e3d97a63b7
Revises: 
Create Date: 2024-04-30 23:40:16.693528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24e3d97a63b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'students',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=50), nullable=True),
        sa.Column('institution', sa.String(length=50), nullable=True),
        sa.Column('code', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('students')