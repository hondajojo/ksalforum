"""add node plane

Revision ID: 623c73285df
Revises: b66ec21fa51
Create Date: 2015-11-10 17:04:58.818576

"""

# revision identifiers, used by Alembic.
revision = '623c73285df'
down_revision = 'b66ec21fa51'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plane',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plane')
    ### end Alembic commands ###
