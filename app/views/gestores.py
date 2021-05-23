from werkzeug.security import generate_password_hash
from app import db
from flask import request,jsonify
from ..models import Gestores, gestor_schema, gestores_schema

import traceback

def post_gestor():
    body = request.get_json()

    gestores_objetos = Gestores.query.limit(1).all()
    if(gestores_objetos):
        return jsonify({'message' : 'Cadastro Inválido.'}), 400
   
    #Deve possuir pelo menos: nome do estabelecimento, email e senha
    if ("nome_estabelecimento" not in body):
        return jsonify({'message' : 'É necessário o nome do estabelecimento.', 'data' : {}}), 400
    if ("email" not in body):
        return jsonify({'message' : 'É necessário o email.', 'data' : {}}), 400
    if ("senha" not in body):
        return jsonify({'message' : 'É necessário a senha.', 'data' : {}}), 400
    
    p_hash = generate_password_hash(body['senha'])
    gestor = Gestores(nome_estabelecimento=body['nome_estabelecimento'], email = body['email'], senha = p_hash)
    
    try:
        db.session.add(gestor)
        db.session.commit()
        result = gestor_schema.dump(gestor)
        print(result)
        return jsonify({'message' : 'Gestor cadastrado com sucesso.' , 'data': result}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'message' : 'Não foi possível criar um gestor', 'data' : {}}), 500

def gestor_by_email(email):
    try:
        return Gestores.query.filter(Gestores.email == email).one()
    except:
        return None
