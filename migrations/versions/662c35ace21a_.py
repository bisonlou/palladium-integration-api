"""empty message

Revision ID: 662c35ace21a
Revises: 77d60eb5d875
Create Date: 2020-02-14 14:52:20.179292

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '662c35ace21a'
down_revision = '77d60eb5d875'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stationery_requisitions', sa.Column('requisition_date', sa.DateTime(), nullable=False))
    op.alter_column('stationery_requisitions', 'approved_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('stationery_requisitions', 'authorized_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('stationery_requisitions', 'issued_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('stationery_requisitions', 'order_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stationery_requisitions', sa.Column('order_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.alter_column('stationery_requisitions', 'issued_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('stationery_requisitions', 'authorized_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('stationery_requisitions', 'approved_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('stationery_requisitions', 'requisition_date')
    # ### end Alembic commands ###