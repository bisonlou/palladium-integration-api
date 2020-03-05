"""empty message

Revision ID: a009678b7bd3
Revises: 72dcfdcbe74d
Create Date: 2020-03-05 11:39:51.926918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a009678b7bd3'
down_revision = '72dcfdcbe74d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('associate_consultants_name_fkey', 'associate_consultants', type_='foreignkey')
    op.drop_column('projects', 'project_duration')
    op.drop_constraint('stationery_requisitions_authorized_by_fkey', 'stationery_requisitions', type_='foreignkey')
    op.drop_constraint('stationery_requisitions_approved_by_fkey', 'stationery_requisitions', type_='foreignkey')
    op.drop_constraint('stationery_requisitions_issued_by_fkey', 'stationery_requisitions', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('stationery_requisitions_issued_by_fkey', 'stationery_requisitions', 'users', ['issued_by'], ['id'])
    op.create_foreign_key('stationery_requisitions_approved_by_fkey', 'stationery_requisitions', 'users', ['approved_by'], ['id'])
    op.create_foreign_key('stationery_requisitions_authorized_by_fkey', 'stationery_requisitions', 'users', ['authorized_by'], ['id'])
    op.add_column('projects', sa.Column('project_duration', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('associate_consultants_name_fkey', 'associate_consultants', 'users', ['name'], ['id'])
    # ### end Alembic commands ###
