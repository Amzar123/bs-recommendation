"""create table student

Revision ID: 75fe356a34fc
Revises: 
Create Date: 2024-04-30 23:05:47.321348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75fe356a34fc'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
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
    op.drop_table('student')
