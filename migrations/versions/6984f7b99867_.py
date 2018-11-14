"""empty message

Revision ID: 6984f7b99867
Revises: e99c30c25f2c
Create Date: 2018-11-14 10:51:22.858938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6984f7b99867'
down_revision = 'e99c30c25f2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('members', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'members')
    # ### end Alembic commands ###
