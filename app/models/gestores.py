from app import db, ma

class Gestores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome_estabelecimento = db.Column(db.String(255))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))

class GestoresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome_estabelecimento', 'email', 'senha')


gestor_schema = GestoresSchema()
gestores_schema = GestoresSchema(many = True)

