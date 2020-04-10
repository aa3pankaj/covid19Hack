"""empty message

Revision ID: 6239f38674d3
Revises: 
Create Date: 2020-04-10 14:55:17.306615

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6239f38674d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Merchant', 'lat',
               existing_type=mysql.DECIMAL(precision=10, scale=10),
               type_=sa.String(length=80),
               existing_nullable=True)
    op.alter_column('Merchant', 'lng',
               existing_type=mysql.DECIMAL(precision=10, scale=10),
               type_=sa.String(length=80),
               existing_nullable=True)
    op.alter_column('normal_user', 'lat',
               existing_type=mysql.DECIMAL(precision=10, scale=10),
               type_=sa.String(length=80),
               existing_nullable=True)
    op.alter_column('normal_user', 'lng',
               existing_type=mysql.DECIMAL(precision=10, scale=10),
               type_=sa.String(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('normal_user', 'lng',
               existing_type=sa.String(length=80),
               type_=mysql.DECIMAL(precision=10, scale=10),
               existing_nullable=True)
    op.alter_column('normal_user', 'lat',
               existing_type=sa.String(length=80),
               type_=mysql.DECIMAL(precision=10, scale=10),
               existing_nullable=True)
    op.alter_column('Merchant', 'lng',
               existing_type=sa.String(length=80),
               type_=mysql.DECIMAL(precision=10, scale=10),
               existing_nullable=True)
    op.alter_column('Merchant', 'lat',
               existing_type=sa.String(length=80),
               type_=mysql.DECIMAL(precision=10, scale=10),
               existing_nullable=True)
    # ### end Alembic commands ###
