"""empty message

Revision ID: 39c55dd9935a
Revises: d88d652e6754
Create Date: 2021-07-12 13:46:26.642796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39c55dd9935a'
down_revision = 'd88d652e6754'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('tracking_number', sa.String(length=50), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('status_description', sa.String(length=255), nullable=True),
    sa.Column('ship_date', sa.DateTime(), nullable=True),
    sa.Column('estimated_delivery_date', sa.DateTime(), nullable=True),
    sa.Column('actual_delivery_date', sa.DateTime(), nullable=True),
    sa.Column('exception_description', sa.String(length=255), nullable=True),
    sa.Column('carrier', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('occured_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('city_locality', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=True),
    sa.Column('postal_code', sa.String(length=10), nullable=True),
    sa.Column('signer', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('package')
    # ### end Alembic commands ###