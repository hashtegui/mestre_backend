"""adicionando table pedidos

Revision ID: 2bf9d4b7d4b3
Revises: 04bbbc8088e1
Create Date: 2024-01-18 18:12:25.095684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf9d4b7d4b3'
down_revision: Union[str, None] = '04bbbc8088e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pedidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('tenant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('schema_name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('schema_name'),
    schema='shared'
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='shared'
    )
    op.drop_table('teste')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teste',
    sa.Column('column1', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_table('user', schema='shared')
    op.drop_table('tenant', schema='shared')
    op.drop_table('pedidos', schema='public')
    # ### end Alembic commands ###
