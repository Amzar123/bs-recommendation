"""create table test teachers

Revision ID: d56d4647cb20
Revises: 24e3d97a63b7
Create Date: 2024-04-30 23:40:20.660572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd56d4647cb20'
down_revision = '24e3d97a63b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'teachers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=50), nullable=True),
        sa.Column('code', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('teachers')

