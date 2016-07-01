"""empty message

Revision ID: be4c7f23c3a8
Revises: None
Create Date: 2016-06-30 17:25:54.766147

"""

# revision identifiers, used by Alembic.
revision = 'be4c7f23c3a8'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('tamanho_atual', sa.String(), nullable=False))
    op.add_column('result', sa.Column('tempo_importacao', sa.Integer(), nullable=False))
    op.add_column('result', sa.Column('total_tabelas', sa.String(), nullable=False))
    op.add_column('result', sa.Column('ultima_tabela', sa.String(), nullable=False))
    op.drop_column('result', 'msg')
    op.drop_column('result', 'output')
    op.drop_column('result', 'identifier')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('identifier', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('result', sa.Column('output', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('result', sa.Column('msg', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('result', 'ultima_tabela')
    op.drop_column('result', 'total_tabelas')
    op.drop_column('result', 'tempo_importacao')
    op.drop_column('result', 'tamanho_atual')
    ### end Alembic commands ###
