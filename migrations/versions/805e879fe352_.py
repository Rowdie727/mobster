"""empty message

Revision ID: 805e879fe352
Revises: abc3f578166c
Create Date: 2022-01-04 17:14:52.744095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '805e879fe352'
down_revision = 'abc3f578166c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user__stats', sa.Column('user_total_missions_complete', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user__stats', 'user_total_missions_complete')
    # ### end Alembic commands ###