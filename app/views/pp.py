from app.models.gestores import Gestores
from werkzeug.security import generate_password_hash
from werkzeug.wrappers import response
from app import db
from flask import request,jsonify
from ..models.pp import Products, Orders, Clientes, Ordersproducts, product_schema, products_schema, order_schema, orders_schema
#from ..models.clientes import Clientes, cliente_schema

import traceback

def post_product():
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

    produto = Products(preco = body['preco'], categoria = body['categoria'], quantidade = body['quantidade'])
    
    try:
        db.session.add(produto)
        db.session.commit()
        result = product_schema.dump(produto)
        print(result)
        return jsonify({'message' : 'Produto cadastrado com sucesso.' , 'data': result}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'message' : 'Não foi possível cadastra o produto.', 'data' : {}}), 500

def post_order():
    #verificar o gestor
    body = request.get_json()

    #verificar o cliente do pedido
    cliente_obj = Clientes.query.filter_by(email=body['email']).first()
    if not cliente_obj:
        return jsonify({'message' : 'Não foi possível realizar o pedido, cliente não cadastrado.', 'data' : {}}), 500
    
    #verficar os produtos
    precoTotal = 0.0
    for p  in body['products']:
        produto_obj = Products.query.filter_by(id=p['id']).first()
        if not produto_obj:
            return jsonify({'message' : 'Não foi possível realizar o pedido, produto não cadastrado.', 'data' : {}}), 500
        
        produto = product_schema.dump(produto_obj)
        precoTotal = precoTotal + (produto['preco'] * p['quantidade'])
    
    pedido_obj = Orders(valorT=precoTotal, status='criado', cliente_email=body['email'])
    db.session.add(pedido_obj)
    db.session.commit()

    for p  in body['products']:
        produto_obj = Products.query.filter_by(id=p['id']).first()
        pedido_obj.products.append(produto_obj)    
    db.session.commit()

    pedido = order_schema.dump(pedido_obj)
    for p in body['products']:
        order_prod = Ordersproducts.query.filter_by(order_id = pedido['id'], product_id = p['id']).first()
        order_prod.quant_prod = p['quantidade']
        db.session.add(order_prod)
    db.session.commit()
    produtos_json = [pro.to_json() for pro in pedido_obj.products]

    return jsonify({'message' : 'Pedido cadastrado com sucesso.' , 'data': {"id":pedido['id'], 
    'Valor Total': precoTotal, 'produtos': produtos_json, 'status':pedido['status']}}), 201

def get_orders(email):
    #body = request.get_json()

    #verificar o cliente do pedido
    cliente_obj = Clientes.query.filter_by(email=email).first()
    if not cliente_obj:
        return jsonify({'message' : 'Não foi possível realizar o pedido, cliente não cadastrado.', 'data' : {}}), 500
    
    resp = [orde.to_json() for orde in cliente_obj.orders]

    return jsonify({'data': resp}), 200

def put_order(id):
    order_obj = Orders.query.filter_by(id=id).first()

    if order_schema.dump(order_obj)['status'] == 'cancelado':
        return jsonify({'message' : 'Pedido já se encontra cancelado.', 'data' : {}}), 200
    if order_schema.dump(order_obj)['status'] == 'finalizado':
        return jsonify({'message' : 'Pedido já se encontra finalizado.', 'data' : {}}), 200

    body = request.get_json()
    #verificar se é gestor ou cliente
    gestor_obj = Gestores.query.filter_by(email=body['email']).one_or_none()
    if gestor_obj:
        status = body['status']

        #Verifica se é um status válido
        if (status not in ('preparando', 'finalizado', 'cancelado')):
            return jsonify({'message' : 'Status inválido. ', 'data' : {}}), 400
        
        #Cancela somente se não tiver produto em estoque
        if (status in('cancelado')):
            #verifica estoque
            for pro in products_schema.dump(order_obj.products):
                quant_estoque = product_schema.dump((Products.query.filter_by(id=pro['id']).first()))['quantidade']
                quant_pedido = Ordersproducts.query.filter_by(order_id = order_schema.dump(order_obj)['id'], product_id = pro['id']).first().to_json()['quant_prod']

                if quant_pedido > quant_estoque:
                    order_obj.status = 'cancelado'
                    db.session.add(order_obj)
                    db.session.commit()
                    return jsonify({'message' : 'Status do pedido modificado para cancelado.', 'data' : {}}), 200
        if (status == 'preparando' and order_schema.dump(order_obj)['status'] == 'criado'):
            order_obj.status = 'preparando'
            db.session.add(order_obj)
            db.session.commit()
            return jsonify({'message' : 'Status do pedido modificado para preparando.', 'data' : {}}), 200
        if (status == 'finalizado' and order_schema.dump(order_obj)['status'] == 'preparando'):
            order_obj.status = 'finalizado'
            db.session.add(order_obj)
            db.session.commit()
            return jsonify({'message' : 'Status do pedido modificado para finalizado.', 'data' : {}}), 200
        
        return jsonify({'message' : 'Não foi possível alterar o status do pedido.', 'data' : {}}), 400
    
    cliente_obj = Clientes.query.filter_by(email=body['email']).one_or_none()
    if cliente_obj:
        #verifica se o pedido é realmente do cliente
        pedidos_c = cliente_obj.orders.filter_by(id = id).first()
        if pedidos_c and order_schema.dump(pedidos_c)['status'] == 'criado':
            order_obj.status = 'cancelado'
            db.session.add(order_obj)
            db.session.commit()
            return jsonify({'message' : 'Status do pedido modificado para cancelado.', 'data' : {}}), 200
        else:
            return jsonify({'message' : 'Não foi possível alterar o status do pedido.', 'data' : {}}), 400

    return jsonify({'message' : 'usuário inválido.', 'data' : {}}), 400

def test():
    ...

