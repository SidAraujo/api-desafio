from app import app
from flask import request
from ..views import gestores, clientes, produtos

@app.route('/gestores', methods=['POST'])
def post_gestor():
    return gestores.post_gestor()

@app.route('/clientes', methods = ['POST'])
def post_cliente():
    return clientes.post_cliente()

@app.route('/produtos', methods=['POST'])
def post_produtos():
    return produtos.post_produto()