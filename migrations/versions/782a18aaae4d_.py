"""empty message

Revision ID: 782a18aaae4d
Revises: 23ec3edd76e5
Create Date: 2018-11-15 12:26:27.523408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '782a18aaae4d'
down_revision = '23ec3edd76e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('class_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'group', 'class', ['class_id'], ['id'])
    op.drop_column('group', 'class_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('class_name', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column('group', 'class_id')
    # ### end Alembic commands ###
