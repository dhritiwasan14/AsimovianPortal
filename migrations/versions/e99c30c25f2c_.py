"""empty message

Revision ID: e99c30c25f2c
Revises: 2e32747114a2
Create Date: 2018-11-14 10:50:37.781181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e99c30c25f2c'
down_revision = '2e32747114a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('members', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'members')
    # ### end Alembic commands ###
