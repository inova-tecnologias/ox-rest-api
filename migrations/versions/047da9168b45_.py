"""empty message

Revision ID: 047da9168b45
Revises: d4061d895922
Create Date: 2020-10-17 20:15:11.162954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '047da9168b45'
down_revision = 'd4061d895922'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('changed', sa.DateTime(), nullable=True))
    op.add_column('customer', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'created')
    op.drop_column('customer', 'changed')
    # ### end Alembic commands ###
