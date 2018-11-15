"""empty message

Revision ID: b429572df7aa
Revises: 6984f7b99867
Create Date: 2018-11-14 15:39:37.822164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b429572df7aa'
down_revision = '6984f7b99867'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'group', sa.Column('class_name', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'group', 'class', ['class_name'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column(u'group', 'class_name')
    op.drop_table('class')
    # ### end Alembic commands ###
