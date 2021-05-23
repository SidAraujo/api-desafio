from app import app
from flask import request
from ..views import gestores, clientes, pp

@app.route('/gestores', methods=['POST'])
def post_gestor():
    return gestores.post_gestor()

@app.route('/clientes', methods = ['POST'])
def post_cliente():
    return clientes.post_cliente()

@app.route('/products', methods = ['POST'])
def post_product():
    return pp.post_product()

@app.route('/orders', methods=['POST'])
def post_order():
    return pp.post_order()

@app.route('/orders/<email>', methods=['GET'])
def get_orders(email):
    return pp.get_orders(email)

@app.route('/orders/<id>', methods=['PUT'])
def put_order(id):
   return pp.put_order(id) 

@app.route('/test', methods = ['POST'])
def test():
    return pp.test()