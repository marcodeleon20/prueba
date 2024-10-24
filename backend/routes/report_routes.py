from flask import Blueprint, jsonify, request
from models import Purchase, User, Product
from flask_jwt_extended import jwt_required

report_bp = Blueprint('report', __name__)


@report_bp.route('/purchases', methods=['GET'])
def get_purchase_report():

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401

  
    headers = {
        'Authorization': f'Bearer {token}'
    }

 
    purchases = Purchase.query.all()


    result = [
        {
            "cliente": User.query.get(purchase.user_id).username,  
            "fecha_compra": purchase.date.strftime("%Y-%m-%d %H:%M:%S"),  
            "producto": {
                "nombre": Product.query.get(purchase.product_id).name,  
                "cantidad": purchase.quantity,  
                "precio": Product.query.get(purchase.product_id).precio  
            }
        } for purchase in purchases
    ]
    
    return jsonify(result)
