"""empty message

Revision ID: ef1c115b6195
Revises: b828e4e1c284
Create Date: 2018-11-18 19:25:19.455452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef1c115b6195'
down_revision = 'b828e4e1c284'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'group', 'class', ['class_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'group', type_='foreignkey')
    # ### end Alembic commands ###
