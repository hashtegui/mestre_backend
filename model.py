import datetime
import decimal
import uuid
from typing import List, Optional

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Double,
                        ForeignKeyConstraint, Index, Integer, Numeric,
                        PrimaryKeyConstraint, String, Table, Text, Uuid, text)
from sqlalchemy.dialects.postgresql import OID, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PrismaMigrations(Base):
    __tablename__ = '_prisma_migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='_prisma_migrations_pkey'),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    checksum: Mapped[str] = mapped_column(String(64))
    migration_name: Mapped[str] = mapped_column(String(255))
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    applied_steps_count: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    finished_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    logs: Mapped[Optional[str]] = mapped_column(Text)
    rolled_back_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))


class Cliente(Base):
    __tablename__ = 'cliente'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='cliente_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgc: Mapped[str] = mapped_column(String(15))
    nome: Mapped[Optional[str]] = mapped_column(String(100))
    razao_social: Mapped[Optional[str]] = mapped_column(String(150))
    tipo_pessoa: Mapped[Optional[str]] = mapped_column(String(1))
    usuario_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    fornecedor: Mapped[List['Fornecedor']] = relationship('Fornecedor', back_populates='cliente')
    filial: Mapped[List['Filial']] = relationship('Filial', back_populates='cliente')


class Departamento(Base):
    __tablename__ = 'departamento'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='departamento_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(50))
    referencia: Mapped[Optional[str]] = mapped_column(String(10))

    secao: Mapped[List['Secao']] = relationship('Secao', back_populates='departamento')
    produto: Mapped[List['Produto']] = relationship('Produto', back_populates='departamento')


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('blk_read_time', Double(53)),
    Column('blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Unidade(Base):
    __tablename__ = 'unidade'
    __table_args__ = (
        PrimaryKeyConstraint('unidade', name='unidade_pkey'),
    )

    unidade: Mapped[str] = mapped_column(String(4), primary_key=True)
    descricao: Mapped[str] = mapped_column(String(60))

    produto: Mapped[List['Produto']] = relationship('Produto', foreign_keys='[Produto.unidade_cx_id]', back_populates='unidade_cx')
    produto_: Mapped[List['Produto']] = relationship('Produto', foreign_keys='[Produto.unidade_id]', back_populates='unidade')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        ForeignKeyConstraint(['usuarioId'], ['usuario.id'], ondelete='SET NULL', onupdate='CASCADE', name='usuario_usuarioId_fkey'),
        PrimaryKeyConstraint('id', name='usuario_pkey'),
        Index('usuario_login_key', 'login', unique=True)
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    login: Mapped[str] = mapped_column(String(50))
    senha: Mapped[str] = mapped_column(String(100))
    setor: Mapped[str] = mapped_column(String(20))
    usuarioId: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    usuario: Mapped['Usuario'] = relationship('Usuario', remote_side=[id], back_populates='usuario_reverse')
    usuario_reverse: Mapped[List['Usuario']] = relationship('Usuario', remote_side=[usuarioId], back_populates='usuario')
    pedido_venda: Mapped[List['PedidoVenda']] = relationship('PedidoVenda', back_populates='usuario')
    produto: Mapped[List['Produto']] = relationship('Produto', back_populates='usuario')


class Fornecedor(Base):
    __tablename__ = 'fornecedor'
    __table_args__ = (
        ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name='fornecedor_cliente_id_fkey'),
        PrimaryKeyConstraint('id', name='fornecedor_pkey'),
        Index('fornecedor_cliente_id_key', 'cliente_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgc: Mapped[str] = mapped_column(String(15))
    razao_social: Mapped[str] = mapped_column(String(150))
    nome_fantasia: Mapped[Optional[str]] = mapped_column(String(150))
    tipo_pessoa: Mapped[Optional[str]] = mapped_column(String(1))
    cliente_id: Mapped[Optional[int]] = mapped_column(Integer)

    cliente: Mapped['Cliente'] = relationship('Cliente', back_populates='fornecedor')
    filial: Mapped[List['Filial']] = relationship('Filial', back_populates='fornecedor')
    produto: Mapped[List['Produto']] = relationship('Produto', back_populates='fornecedor')


class PedidoVenda(Base):
    __tablename__ = 'pedido_venda'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='SET NULL', onupdate='CASCADE', name='pedido_venda_usuario_id_fkey'),
        PrimaryKeyConstraint('id', name='pedido_venda_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dt_pedido: Mapped[datetime.date] = mapped_column(Date)
    obs: Mapped[str] = mapped_column(String(200))
    valor_total: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    nome_cliente: Mapped[Optional[str]] = mapped_column(String(255))
    valor_desconto: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    valor_frete: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    forma_pagamento: Mapped[Optional[str]] = mapped_column(String(50))
    usuario_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    status: Mapped[Optional[str]] = mapped_column(String(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='pedido_venda')
    pedido_venda_item: Mapped[List['PedidoVendaItem']] = relationship('PedidoVendaItem', back_populates='pedido')


class Secao(Base):
    __tablename__ = 'secao'
    __table_args__ = (
        ForeignKeyConstraint(['departamento_id'], ['departamento.id'], name='fk_secao_depto'),
        PrimaryKeyConstraint('id', name='secao_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[Optional[str]] = mapped_column(String(50))
    referencia: Mapped[Optional[str]] = mapped_column(String(10))
    departamento_id: Mapped[Optional[int]] = mapped_column(Integer)

    departamento: Mapped['Departamento'] = relationship('Departamento', back_populates='secao')
    categoria: Mapped[List['Categoria']] = relationship('Categoria', back_populates='secao')
    produto: Mapped[List['Produto']] = relationship('Produto', back_populates='secao')


class Categoria(Base):
    __tablename__ = 'categoria'
    __table_args__ = (
        ForeignKeyConstraint(['secao_id'], ['secao.id'], name='fk_cat_secao'),
        PrimaryKeyConstraint('id', name='categoria_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(50))
    secao_id: Mapped[Optional[int]] = mapped_column(Integer)

    secao: Mapped['Secao'] = relationship('Secao', back_populates='categoria')
    produto: Mapped[List['Produto']] = relationship('Produto', back_populates='categoria')


class Filial(Base):
    __tablename__ = 'filial'
    __table_args__ = (
        ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name='filial_cliente_id_fkey'),
        ForeignKeyConstraint(['fornecedor_id'], ['fornecedor.id'], name='filial_fornecedor_id_fkey'),
        PrimaryKeyConstraint('id', name='filial_pkey'),
        Index('filial_cliente_id_key', 'cliente_id', unique=True),
        Index('filial_fornecedor_id_key', 'fornecedor_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgc: Mapped[str] = mapped_column(String(15))
    razao_social: Mapped[str] = mapped_column(String(100))
    nome_filial: Mapped[Optional[str]] = mapped_column(String(100))
    cliente_id: Mapped[Optional[int]] = mapped_column(Integer)
    fornecedor_id: Mapped[Optional[int]] = mapped_column(Integer)

    cliente: Mapped['Cliente'] = relationship('Cliente', back_populates='filial')
    fornecedor: Mapped['Fornecedor'] = relationship('Fornecedor', back_populates='filial')
    estoque: Mapped[List['Estoque']] = relationship('Estoque', back_populates='filial')


class Produto(Base):
    __tablename__ = 'produto'
    __table_args__ = (
        ForeignKeyConstraint(['categoria_id'], ['categoria.id'], name='fk_produto_cat'),
        ForeignKeyConstraint(['departamento_id'], ['departamento.id'], name='fk_produto_depto'),
        ForeignKeyConstraint(['fornecedor_id'], ['fornecedor.id'], name='fk_produto_fornecedor'),
        ForeignKeyConstraint(['secao_id'], ['secao.id'], name='fk_produto_sec'),
        ForeignKeyConstraint(['unidade_cx_id'], ['unidade.unidade'], name='fk_produto_unidadecx'),
        ForeignKeyConstraint(['unidade_id'], ['unidade.unidade'], name='fk_produto_unidade'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='SET NULL', onupdate='CASCADE', name='produto_usuario_id_fkey'),
        PrimaryKeyConstraint('id', name='produto_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(60))
    cod_barras: Mapped[Optional[str]] = mapped_column(String(20))
    cod_barras_cx: Mapped[Optional[str]] = mapped_column(String(20))
    cod_fabrica: Mapped[Optional[str]] = mapped_column(String(10))
    custo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    dt_cadastro: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6), server_default=text('CURRENT_TIMESTAMP'))
    dt_exclusao: Mapped[Optional[datetime.date]] = mapped_column(Date)
    qt_estoque: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    markup: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    preco_venda: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    qt_unit: Mapped[Optional[int]] = mapped_column(Integer)
    qt_unit_cx: Mapped[Optional[int]] = mapped_column(Integer)
    categoria_id: Mapped[Optional[int]] = mapped_column(Integer)
    departamento_id: Mapped[Optional[int]] = mapped_column(Integer)
    fornecedor_id: Mapped[Optional[int]] = mapped_column(Integer)
    secao_id: Mapped[Optional[int]] = mapped_column(Integer)
    unidade_id: Mapped[Optional[str]] = mapped_column(String(4))
    unidade_cx_id: Mapped[Optional[str]] = mapped_column(String(4))
    usuario_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    categoria: Mapped['Categoria'] = relationship('Categoria', back_populates='produto')
    departamento: Mapped['Departamento'] = relationship('Departamento', back_populates='produto')
    fornecedor: Mapped['Fornecedor'] = relationship('Fornecedor', back_populates='produto')
    secao: Mapped['Secao'] = relationship('Secao', back_populates='produto')
    unidade_cx: Mapped['Unidade'] = relationship('Unidade', foreign_keys=[unidade_cx_id], back_populates='produto')
    unidade: Mapped['Unidade'] = relationship('Unidade', foreign_keys=[unidade_id], back_populates='produto_')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='produto')
    estoque: Mapped[List['Estoque']] = relationship('Estoque', back_populates='produto')
    pedido_venda_item: Mapped[List['PedidoVendaItem']] = relationship('PedidoVendaItem', back_populates='produto')


class Estoque(Base):
    __tablename__ = 'estoque'
    __table_args__ = (
        ForeignKeyConstraint(['filial_id'], ['filial.id'], name='estoque_filial_id_fkey'),
        ForeignKeyConstraint(['produto_id'], ['produto.id'], name='estoque_produto_id_fkey'),
        PrimaryKeyConstraint('id', name='estoque_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filial_id: Mapped[int] = mapped_column(Integer)
    produto_id: Mapped[int] = mapped_column(Integer)
    quantidade_estoque: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    quantidade_estoque_geral: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    quantidade_reservada: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))

    filial: Mapped['Filial'] = relationship('Filial', back_populates='estoque')
    produto: Mapped['Produto'] = relationship('Produto', back_populates='estoque')


class PedidoVendaItem(Base):
    __tablename__ = 'pedido_venda_item'
    __table_args__ = (
        ForeignKeyConstraint(['pedido_id'], ['pedido_venda.id'], name='fk_pedido'),
        ForeignKeyConstraint(['produto_id'], ['produto.id'], name='fk_produto'),
        PrimaryKeyConstraint('numero_sequencia', name='pedido_venda_item_pkey')
    )

    numero_sequencia: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_total: Mapped[decimal.Decimal] = mapped_column(Numeric(28, 8))
    valor_unitario: Mapped[decimal.Decimal] = mapped_column(Numeric(28, 8))
    pedido_id: Mapped[int] = mapped_column(Integer)
    produto_id: Mapped[int] = mapped_column(Integer)
    codbarras: Mapped[Optional[str]] = mapped_column(String(255))
    desconto: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 2))
    numero_item: Mapped[Optional[int]] = mapped_column(Integer)
    quantidade: Mapped[Optional[int]] = mapped_column(Integer)
    preco_venda: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(28, 8))

    pedido: Mapped['PedidoVenda'] = relationship('PedidoVenda', back_populates='pedido_venda_item')
    produto: Mapped['Produto'] = relationship('Produto', back_populates='pedido_venda_item')
