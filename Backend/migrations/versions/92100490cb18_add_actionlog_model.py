"""Add ActionLog model

Revision ID: 92100490cb18
Revises: 63ecd53788a3
Create Date: 2024-12-31 09:39:48.812603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92100490cb18'
down_revision = '63ecd53788a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=50), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['admin_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('action_logs')
    # ### end Alembic commands ###
