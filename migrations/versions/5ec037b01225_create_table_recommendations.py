"""create table recommendations

Revision ID: 5ec037b01225
Revises: 4f6394a6e24c
Create Date: 2024-04-30 23:48:22.258510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ec037b01225'
down_revision = '4f6394a6e24c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recommendations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('recommendation', sa.String(length=50), nullable=True),
        sa.Column('student_id', sa.String(), sa.ForeignKey('students.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('recommendations')