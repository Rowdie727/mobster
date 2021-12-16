"""empty message

Revision ID: e7b5ae768f27
Revises: e2208a636edc
Create Date: 2021-11-28 00:51:29.636699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7b5ae768f27'
down_revision = 'e2208a636edc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user__stats', sa.Column('user_current_health', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user__stats', 'user_current_health')
    # ### end Alembic commands ###