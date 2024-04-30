"""create table test questions

Revision ID: c8edb65e8301
Revises: d56d4647cb20
Create Date: 2024-04-30 23:40:25.637617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8edb65e8301'
down_revision = 'd56d4647cb20'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'questions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('question', sa.String(length=50), nullable=True),
        sa.Column('key_answer', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('questions')
    
