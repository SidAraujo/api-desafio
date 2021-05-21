from app import db
from flask import request,jsonify
from ..models.produtos import Produtos, produto_schema, produtos_schema

import traceback

def post_produto():
    body = request.get_json()

    #Verificar se é o gestor que está cadastrando
   
    #Deve possuir pelo menos: nome do estabelecimento, email e senha
    #Contruir uma msg com as colunas não presentes
    if ("preco" not in body):
        return jsonify({'message' : 'É necessário o preço do produto.', 'data' : {}}), 400
    print(body['categoria'])
    if ("categoria" not in body):
        return jsonify({'message' : 'É necessário a categoria.', 'data' : {}}), 400
    if ("quantidade" not in body):
        return jsonify({'message' : 'É necessário a quantidade do produto.', 'data' : {}}), 400
    
    #Verificar se possui categoria correta

    produto = Produtos(preco = body['preco'], categoria = body['categoria'], quantidade = body['quantidade'])
    
    try:
        db.session.add(produto)
        db.session.commit()
        result = produto_schema.dump(produto)
        print(result)
        return jsonify({'message' : 'Produto cadastrado com sucesso.' , 'data': result}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'message' : 'Não foi possível cadastra o produto.', 'data' : {}}), 500
