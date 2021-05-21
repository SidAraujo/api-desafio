from app import db, ma

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    preco = db.Column(db.Float)
    categoria = db.Column(db.String(12))
    quantidade = db.Column(db.Integer)

class ProdutosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'preco','categoria', 'quantidade')


produto_schema = ProdutosSchema()
produtos_schema = ProdutosSchema(many = True)