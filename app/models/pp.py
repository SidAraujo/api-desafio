from marshmallow.fields import Integer
from app import db, ma

class Clientes(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    nome = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    senha = db.Column(db.String(100))
    data_nasc = db.Column(db.Date)
    orders = db.relationship('Orders', backref='cliente', lazy='dynamic')


class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('nome', 'email', 'senha', 'telefone', 'data_nasc')

cliente_schema = ClientesSchema()
clientes_schema = ClientesSchema(many = True)

class Ordersproducts(db.Model):
    # __table_args__ = (
    #     db.PrimaryKeyConstraint('order_id', 'product_id'),
    # )
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quant_prod = db.Column(db.Integer)

    def to_json(self):
        return {"order_id" : self.order_id, "product_id" : self.product_id, "quant_prod": self.quant_prod}

    

class Orders(db.Model):
    id = id = db.Column(db.Integer, primary_key = True)
    valorT = db.Column(db.Float)
    status = db.Column(db.String(25))
    cliente_email = db.Column(db.String(100), db.ForeignKey('clientes.email'))
    products = db.relationship('Products', secondary='ordersproducts', backref=db.backref('orders', lazy='dynamic'))

    def to_json(self):
        return {"id" : self.id, "status" : self.status, "Valor Total": self.valorT}

class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    preco = db.Column(db.Float)
    categoria = db.Column(db.String(12))
    quantidade = db.Column(db.Integer)

    def to_json(self):
        return {"id" : self.id, "categoria": self.categoria, "preco": self.preco}


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'preco','categoria', 'quantidade')

class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'valorT','status', 'products')


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many = True)

product_schema = ProductsSchema()
products_schema = ProductsSchema(many = True)