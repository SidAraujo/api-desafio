# API - Desafio Maida

## Bibliotecas utilizadas

- Flask
- Flask SQLAlchemy
- Flask Marshmallow
- Mysqlclient
- PyJWT

## Execução

Abrir console python na pasta do respositório:

* from app import db

* db.create_all()

Após criar o banco executar o arquivo run.py

## Requisitos de Negócios
### Cadastrar o gestor
/gestores _Method_ : POST
- Primeira ação a ser realizada;
- Deve ter nome do estabelecimento, email e senha;
- Não pode ter mais de um gestor cadastrado.

### Cadastrar o cliente
/clientes _Method_ : POST
- É necessário o cadastro para realizar pedidos;
- Deve conter o nome, data de nascimento, telefone, senha e email;
- O identificador é o email.

### Login
Cliente
/login _Method_ : POST
Gestor
/gestor/login _Method_ : POST

- Informar email e senha
- Sessão máxima de 10 minutos


### Cadastrar o produto
/produtos _Method_ : POST
- Somente o gestor cadastra produto
- Deve ter preço e classificação (bebida, comida ou sobremesa)
- Gestor pode editar ou remover produtos
- Adcionado atributo quantidade

### Solicitar pedido
/pedidos _Method_ : POST
- Produtos para o pedido
- Como retorno identificação do pedido, lista de produtos e valor total

### Consultar pedido
/pedidos/<email> _Method_ : GET
- Consulta status e lista de finalizados

### Gerenciar pedido
/pedido/<id> _Method_ : PUT
- Gestor informa status atual do pedido
- Gestor pode finalizar ou cancelar pedido

### Cancelar pedido
/pedido/<id> _Method_ : PUT
- O cliente pode cancelar o pedido se ainda não estiver sendo preparado.



## Pedido
Quando um pedido é solicitado ele fica com status Criado.
O gerente pode modificar esse status para Preparando, Finalizado ou Cancelado.
Para cancelar o pedido não deve ter o produto em estoque

O cliente só pode cancelar o pedido enquanto estiver no status criado.
