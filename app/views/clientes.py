from werkzeug.security import generate_password_hash
from app import db
from flask import request,jsonify
from ..models.pp import Clientes, cliente_schema, clientes_schema

import traceback

def post_cliente():
    #verificar se já existe um gestor cadastrado

    body = request.get_json()

    #Deve possuir pelo menos: nome, email, senha, telefone e data de nascimento
    if ("nome" not in body):
        return jsonify({'message' : 'É necessário o nome do cliente.', 'data' : {}}), 400
    if ("email" not in body):
        return jsonify({'message' : 'É necessário o email.', 'data' : {}}), 400
    if ("senha" not in body):
        return jsonify({'message' : 'É necessário a senha.', 'data' : {}}), 400
    if ("telefone" not in body):
        return jsonify({'message' : 'É necessário o telefone.', 'data' : {}}), 400
    if ("data_nasc" not in body):
        return jsonify({'message' : 'É necessário a data de nascimento.', 'data' : {}}), 400
    
    cliente = Clientes(nome=body['nome'], email = body['email'], senha = body['senha'], telefone = body['telefone'], data_nasc = body['data_nasc'])
    try:
        db.session.add(cliente)
        db.session.commit()
        result = cliente_schema.dump(cliente)
        print(result)
        return jsonify({'message' : 'Cliente cadastrado com sucesso.' , 'data': result}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'message' : 'Não foi possível cadastra o cliente', 'data' : {}}), 500