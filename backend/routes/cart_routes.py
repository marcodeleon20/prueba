from flask import Blueprint, request, jsonify
from models import CartItem, Purchase, db, Product
from datetime import datetime
import requests  

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401

  
    headers = {
        'Authorization': f'Bearer {token}'  
    }

    
    user_id = request.json.get('user_id') 
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')

   
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Producto no encontrado"}), 404
    if product.quantity < quantity:
        return jsonify({"msg": "Cantidad solicitada no disponible en inventario"}), 400


    new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(new_item)

 
    db.session.commit()

    return jsonify({"msg": "Producto añadido al carrito con éxito"}), 200



@cart_bp.route('/confirm', methods=['POST'])
def confirm_purchase():
    # Obtener el token JWT del encabezado de la solicitud
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401


    headers = {
        'Authorization': f'Bearer {token}'  
    }


    user_id = request.json.get('user_id')

    
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"msg": "El carrito está vacío"}), 400


    for item in cart_items:
        product = Product.query.get(item.product_id)

        if not product:
            return jsonify({"msg": f"Producto con ID {item.product_id} no encontrado"}), 404
        

        if product.quantity < item.quantity:
            return jsonify({"msg": f"Cantidad insuficiente para el producto {product.name}"}), 400
        
        # Registrar la compra en la tabla `Purchase`
        new_purchase = Purchase(
            user_id=user_id,
            product_id=product.id,
            quantity=item.quantity,
            date=datetime.utcnow()
        )
        db.session.add(new_purchase)


        product.quantity -= item.quantity


    CartItem.query.filter_by(user_id=user_id).delete()

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({"msg": "Compra confirmada con éxito"}), 200


@cart_bp.route('/', methods=['GET'])
def get_cart():

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401


    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"msg": "Falta el ID de usuario en la solicitud"}), 400


    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"msg": "El carrito está vacío"}), 400


    cart_details = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            cart_details.append({
                'product_id': product.id,
                'name': product.name,
                'price': product.precio,
                'quantity': item.quantity,
                'total': product.precio * item.quantity
            })

    # Devolver la lista de productos en el carrito
    return jsonify(cart_details), 200
