"""change Token.value column

Revision ID: 28eb5afae162
Revises: 51b36c819d5f
Create Date: 2019-12-08 01:05:46.467620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28eb5afae162'
down_revision = '51b36c819d5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_token_value'), 'token', ['value'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_value'), table_name='token')
    # ### end Alembic commands ###
