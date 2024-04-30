"""create table test assesment

Revision ID: b35a5a9b1d24
Revises: 50fedf888d34
Create Date: 2024-04-30 23:46:05.049567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b35a5a9b1d24'
down_revision = '50fedf888d34'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'answers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('answer', sa.String(length=50), nullable=True),
        sa.Column('assessment_id', sa.String(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessment.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('answers')