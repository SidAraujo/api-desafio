# API - Desafio Maida

## Bibliotecas utilizadas

- Flask
- Flask SQLAlchemy
- Flask Marshmallow
- Mysqlclient

# Execução

Console -> python
from app import db

db.create_all()

## Requisitos de Negócios
### Cadastrar o gestor
/gestores _Method_ : POST
- Primeira ação a ser realizada;
- Deve ter nome do estabelecimento, email e senha;
- Não pode ter mais de um gestor cadastrado.

### Cadastrar o cliente
/clientes _Method_ : POST
- É necessário o cadastro para realizar pedidos;
- Deve conter o nome, data de nascimento, telefone e email;
- O identificador é o email.

### Cadastrar o produto
/produtos _Method_ : POST
- Somente o gestor cadastra produto
- Deve ter preço e classificação (bebida, comida ou sobremesa)
- Gestor pode editar ou remover produtos
- Adcionado atributo quantidade