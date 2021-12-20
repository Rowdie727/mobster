"""empty message

Revision ID: 165a53544341
Revises: ed902097b641
Create Date: 2021-12-20 15:31:04.923716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '165a53544341'
down_revision = 'ed902097b641'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user__stats', sa.Column('user_stamina_thread_running', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user__stats', 'user_stamina_thread_running')
    # ### end Alembic commands ###