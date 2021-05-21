# API - Desafio Maida

## Bibliotecas utilizadas

- Flask
- Flask SQLAlchemy
- Flask Marshmallow
- Mysqlclient

# Execução

Console -> python
>> from app import db
>> db.create_all()

## Requisitos de Negócios
### Cadastrar o gestor
/gestor _Method_ : POST
- Primeira ação a ser realizada;
- Deve ter nome do estabelecimento, email e senha;
- Não pode ter mais de um gestor cadastrado.