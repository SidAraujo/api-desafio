from app import db, ma
from . import produtos

class Pedidos(db.Model):
    id = id = db.Column(db.Integer, primary_key = True)
    valorT = db.Column(db.Float)
    status = db.Column(db.String(25))
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))
    produto = db.relationship('Produtos')

class PedidosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'valorT','status', 'produto_id')


pedido_schema = PedidosSchema()
pedidos_schema = PedidosSchema(many = True)