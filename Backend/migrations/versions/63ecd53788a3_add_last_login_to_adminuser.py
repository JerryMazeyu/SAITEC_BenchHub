"""Add last_login to AdminUser

Revision ID: 63ecd53788a3
Revises: 69836087c8f9
Create Date: 2024-12-30 14:43:29.062727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63ecd53788a3'
down_revision = '69836087c8f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_login', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_users', schema=None) as batch_op:
        batch_op.drop_column('last_login')

    # ### end Alembic commands ###