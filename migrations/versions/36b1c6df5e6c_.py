"""empty message

Revision ID: 36b1c6df5e6c
Revises: ca165bdf857d
Create Date: 2021-12-19 04:37:26.673042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b1c6df5e6c'
down_revision = 'ca165bdf857d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user__stats', sa.Column('user_health_thread_running', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user__stats', 'user_health_thread_running')
    # ### end Alembic commands ###
