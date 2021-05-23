from marshmallow.fields import Integer
from app import db, ma

class Gestores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome_estabelecimento = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class GestoresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome_estabelecimento', 'email', 'senha')


gestor_schema = GestoresSchema()
gestores_schema = GestoresSchema(many = True)

class Clientes(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    pedidos = db.relationship('Pedidos', backref='cliente', lazy='dynamic')


class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('nome', 'email', 'senha', 'telefone', 'data_nasc')

cliente_schema = ClientesSchema()
clientes_schema = ClientesSchema(many = True)

class Pedidosprodutos(db.Model):
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    quant_prod = db.Column(db.Integer)

    def to_json(self):
        return {"pedido_id" : self.pedido_id, "produto_id" : self.produto_id, "quant_prod": self.quant_prod}

    

class Pedidos(db.Model):
    id = id = db.Column(db.Integer, primary_key = True)
    valorT = db.Column(db.Float)
    status = db.Column(db.String(25))
    cliente_email = db.Column(db.String(100), db.ForeignKey('clientes.email'))
    produtos = db.relationship('Produtos', secondary='pedidosprodutos', backref=db.backref('pedidos', lazy='dynamic'))

    def to_json(self):
        return {"id" : self.id, "status" : self.status, "Valor Total": self.valorT}

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(12), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"id" : self.id, "categoria": self.categoria, "preco": self.preco}


class ProdutosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'preco','categoria', 'quantidade')

class PedidosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'valorT','status', 'produtos')


pedido_schema = PedidosSchema()
pedidos_schema = PedidosSchema(many = True)

produto_schema = ProdutosSchema()
produtos_schema = ProdutosSchema(many = True)