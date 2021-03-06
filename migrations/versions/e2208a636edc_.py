"""empty message

Revision ID: e2208a636edc
Revises: 11800a770d62
Create Date: 2021-11-26 19:20:30.807726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2208a636edc'
down_revision = '11800a770d62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user__stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_level', sa.Integer(), nullable=False),
    sa.Column('user_experience', sa.Integer(), nullable=False),
    sa.Column('experience_to_level_up', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user__stats')
    # ### end Alembic commands ###
