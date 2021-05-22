from app import db, ma
from . import produtos, pedidos

pedidoprodutos = db.Table('PedidoProduto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedidos.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
)