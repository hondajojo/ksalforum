"""add reply table

Revision ID: 1b395a0e667c
Revises: 623c73285df
Create Date: 2015-11-16 13:19:29.441454

"""

# revision identifiers, used by Alembic.
revision = '1b395a0e667c'
down_revision = '623c73285df'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('up_vote', sa.Integer(), nullable=True),
    sa.Column('down_vote', sa.Integer(), nullable=True),
    sa.Column('last_touched', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reply')
    ### end Alembic commands ###
