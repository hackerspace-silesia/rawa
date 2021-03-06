"""add new model

Revision ID: 301a679a98be
Revises: 28eb5afae162
Create Date: 2019-12-08 07:11:57.787590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301a679a98be'
down_revision = '28eb5afae162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('boughtprize',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('prize_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['prize_id'], ['prize.id'], name=op.f('fk_boughtprize_prize_id_prize')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_boughtprize_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_boughtprize'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boughtprize')
    # ### end Alembic commands ###
