"""added image path column to animals table

Revision ID: f6534fe44b96
Revises: 
Create Date: 2024-04-10 11:18:26.492913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6534fe44b96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=300), nullable=True))

    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DATETIME(), nullable=True))

    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
