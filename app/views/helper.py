from app.views.clientes import cliente_by_email
from app.views.gestores import gestor_by_email
import jwt
from werkzeug.security import check_password_hash
from flask import request,jsonify
from functools import wraps
from ..models import cliente_schema
import datetime
from app import app
import traceback

def auth():
    body = request.get_json()

    if not body or ("email" not in body) or ("senha" not in body):
        return jsonify({'message' : 'Não foi possível verificar.', 'WWW-Authenticate' : 'Basic auth="Login required"'}), 401
    
    cliente = cliente_by_email(body['email'])
    if not cliente:
        return jsonify({'message' : 'Cliente não encontrado.', 'data':{}}), 401
    
    #colocar hash
    if cliente and check_password_hash(cliente.senha, body['senha']):
        token = jwt.encode({'email':cliente.email, 'exp' : datetime.datetime.now() +  datetime.timedelta(hours=3, minutes=10)}, 
        app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Validado com sucesso.', 'token': token,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=3, minutes=10)})
    
    return jsonify({'message' : 'Não foi possível verificar.', 'WWW-Authenticate' : 'Basic auth="Login required"'}), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.args.get('token')
        body = request.get_json()
        if body == None:
            return jsonify({'message' : 'É necessário um token.', 'data' : {}}), 401
        if (not 'token' in body):
            return jsonify({'message' : 'É necessário um token.', 'data' : {}}), 401
        token = body['token']
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_cliente = cliente_by_email(email=data['email'])
            if current_cliente == None:
                return jsonify({'message' : 'Token do cliente inválido ou expirado', 'data' : {}}), 401
        except Exception:
            traceback.print_exc()
            return jsonify({'message' : 'Token inválido ou expirado', 'data' : {}}), 401
        return f(current_cliente, *args, **kwargs)
    return decorated

def auth_gestor():
    body = request.get_json()

    if not body or ("email" not in body) or ("senha" not in body):
        return jsonify({'message' : 'Não foi possível verificar.', 'WWW-Authenticate' : 'Basic auth="Login required"'}), 401
    
    gestor = gestor_by_email(body['email'])
    if not gestor:
        return jsonify({'message' : 'Gestor não encontrado.', 'data':{}}), 401
    
    #colocar hash
    if gestor and check_password_hash(gestor.senha, body['senha']):
        token = jwt.encode({'email':gestor.email, 'exp' : datetime.datetime.now() +  datetime.timedelta(hours=3, minutes=10)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Validado com sucesso.', 'token': token,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=3, minutes=10)})
    
    return jsonify({'message' : 'Não foi possível verificar.', 'WWW-Authenticate' : 'Basic auth="Login required"'}), 401


def token_gestor_required(f):
    @wraps(f)
    def decorated_gestor(*args, **kwargs):
        body = request.get_json()
        if (not 'token' in body):
            return jsonify({'message' : 'É necessário um token.', 'data' : {}}), 401
        token = body['token']
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")

            current_gestor = gestor_by_email(email=data['email'])
            if current_gestor == None:
                return jsonify({'message' : 'Token do gestor inválido ou expirado', 'data' : {}}), 401
        except Exception:
            traceback.print_exc()
            return jsonify({'message' : 'Token do gestor inválido ou expirado.', 'data' : {}}), 401
        return f(current_gestor, *args, **kwargs)
    return decorated_gestor
    
