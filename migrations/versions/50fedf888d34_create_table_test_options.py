"""create table test options

Revision ID: 50fedf888d34
Revises: c8edb65e8301
Create Date: 2024-04-30 23:45:33.177600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50fedf888d34'
down_revision = 'c8edb65e8301'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'options',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('option', sa.String(length=50), nullable=True),
        sa.Column('question_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('options')
