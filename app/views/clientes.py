from werkzeug.security import generate_password_hash
from app import db
from flask import request,jsonify
from ..models import Clientes, cliente_schema, clientes_schema, Gestores

import traceback

def post_cliente():
    #verificar se já existe um gestor cadastrado
    gestor = Gestores.query.limit(1).all()
    if (not gestor):
        return jsonify({'message' : 'Gestor não cadastrado.'}), 400

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
    p_hash = generate_password_hash(body['senha'])
    cliente = Clientes(nome=body['nome'], email = body['email'], senha = p_hash, telefone = body['telefone'], data_nasc = body['data_nasc'])
    try:
        db.session.add(cliente)
        db.session.commit()
        result = cliente_schema.dump(cliente)
        print(result)
        return jsonify({'message' : 'Cliente cadastrado com sucesso.' , 'data': result}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'message' : 'Não foi possível cadastra o cliente', 'data' : {}}), 500

def cliente_by_email(email):
    try:
        return Clientes.query.filter(Clientes.email == email).one()
    except:
        return None