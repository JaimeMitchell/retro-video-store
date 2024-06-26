"""empty message

Revision ID: f490f5c92121
Revises: 12b07869e062
Create Date: 2024-06-08 06:16:28.656792

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f490f5c92121'
down_revision = '12b07869e062'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('registered_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('registered_at',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###
