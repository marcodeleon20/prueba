from flask import Blueprint, jsonify, request
from models import Product

product_bp = Blueprint('products', __name__)


@product_bp.route('/', methods=['GET'])
def get_products():

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401

   
    headers = {
        'Authorization': f'Bearer {token}'  
    }


    products = Product.query.all()


    result = [
        {
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "price": product.precio,  
            "estado": product.estado,  
            "fecha": product.fecha.strftime("%Y-%m-%dT%H:%M:%S"),  
            "imagen": product.imagen  
        }
        for product in products
    ]
    
    return jsonify(result)
