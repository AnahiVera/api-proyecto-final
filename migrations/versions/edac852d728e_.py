"""empty message

Revision ID: edac852d728e
Revises: dd4b8e9160ad
Create Date: 2024-10-26 11:59:28.011289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edac852d728e'
down_revision = 'dd4b8e9160ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rated', sa.Boolean(), nullable=True))

    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rated', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_postings', schema=None) as batch_op:
        batch_op.drop_column('rated')

    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_column('rated')

    # ### end Alembic commands ###