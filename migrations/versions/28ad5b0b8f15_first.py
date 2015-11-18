"""first

Revision ID: 28ad5b0b8f15
Revises: None
Create Date: 2015-11-09 14:31:02.505179

"""

# revision identifiers, used by Alembic.
revision = '28ad5b0b8f15'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('nickname', sa.Text(), nullable=True),
    sa.Column('avator', sa.Text(), nullable=True),
    sa.Column('signature', sa.Text(), nullable=True),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('website', sa.Text(), nullable=True),
    sa.Column('company', sa.Text(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('reputation', sa.Integer(), nullable=True),
    sa.Column('self_intro', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('twitter', sa.Text(), nullable=True),
    sa.Column('github', sa.Text(), nullable=True),
    sa.Column('douban', sa.Text(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###
