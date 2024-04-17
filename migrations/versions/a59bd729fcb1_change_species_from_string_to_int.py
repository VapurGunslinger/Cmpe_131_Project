"""change species from string to int

Revision ID: a59bd729fcb1
Revises: cf65dbd1e109
Create Date: 2024-04-16 20:51:34.046900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59bd729fcb1'
down_revision = 'cf65dbd1e109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.alter_column('species',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.alter_column('species',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###