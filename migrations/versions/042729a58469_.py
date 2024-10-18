"""empty message

Revision ID: 042729a58469
Revises: d95fd2e31d99
Create Date: 2024-10-18 12:14:08.489235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '042729a58469'
down_revision = 'd95fd2e31d99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'status', ['status_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('status_id')

    # ### end Alembic commands ###