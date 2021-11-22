"""empty message

Revision ID: 11800a770d62
Revises: a769395b6d31
Create Date: 2021-11-22 00:33:24.462343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11800a770d62'
down_revision = 'a769395b6d31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('level_required', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'level_required')
    # ### end Alembic commands ###
