from app import app
from flask import request
from ..views import gestores, clientes, pp, helper

@app.route('/gestores', methods=['POST'])
def post_gestor():
    return gestores.post_gestor()

@app.route('/clientes', methods = ['POST'])
def post_cliente():
    return clientes.post_cliente()

@app.route('/produtos', methods = ['POST'])
@helper.token_gestor_required
def post_protudo(current_gestor):
    return pp.post_produto()

@app.route('/produtos/<id>', methods=['PUT'])
@helper.token_gestor_required
def put_produto(current_gestor, id):
    return pp.put_produto(id)

@app.route('/produtos/<id>', methods=['DELETE'])
@helper.token_gestor_required
def delete_produto(current_gestor, id):
    return pp.delete_produto(id)

@app.route('/pedidos', methods=['POST'])
@helper.token_required
def post_pedido(current_cliente):
    return pp.post_pedido()

@app.route('/pedidos', methods=['GET'])
@helper.token_required
def get_pedidos(current_cliente):
    return pp.get_pedidos()

@app.route('/pedidos/<id>', methods=['PUT'])
def put_pedido(id):
   return pp.put_pedido(id) 

@app.route('/login', methods = ['POST'])
def authenticate():
    return helper.auth()

@app.route('/gestor/login', methods = ['POST'])
def authenticate_gestor():
    return helper.auth_gestor()
