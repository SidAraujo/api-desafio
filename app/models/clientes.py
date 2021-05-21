from app import db, ma

class Clientes(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    nome = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    senha = db.Column(db.String(100))
    data_nasc = db.Column(db.Date)


class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('nome', 'email', 'senha', 'telefone', 'data_nasc')

cliente_schema = ClientesSchema()
clientes_schema = ClientesSchema(many = True)