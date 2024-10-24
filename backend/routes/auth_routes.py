from flask import Blueprint, request, jsonify
import requests
from models import User, Product, db  # Importar el modelo de usuario y la base de datos


auth_bp = Blueprint('auth', __name__)


API_URL = "https://apiexamen.compuflashgt.com/api"
API_KEY = "62245354621022924456"

@auth_bp.route('/login', methods=['POST'])
def login():
   
    user_id = request.json.get('usrId')
    user_password = request.json.get('usrPassword')
    
    # Verificar que se han enviado ambos parámetros
    if not user_id or not user_password:
        return jsonify({"msg": "Faltan parámetros de usuario"}), 400
    

    login_data = {
        "apiKey": API_KEY,
        "usrId": user_id,
        "usrPassword": user_password
    }


    login_response = requests.post(f"{API_URL}/Login", json=login_data)


    if login_response.status_code == 200:
  
        response_data = login_response.json()
        

        username = response_data.get("Usuario")  
        token = response_data.get("Token")  


        user = User.query.filter_by(username=username).first()

        if user:
       
            user.token = token
            user.password = user_password  
        else:
           
            new_user = User(
                username=username,
                password=user_password,
                token=token
            )
            db.session.add(new_user)
            user = new_user  


        db.session.commit()


        return jsonify({
            "response_data": response_data,
            "usuario": {
                "id": user.id,
                "username": user.username,
                "token": user.token
            }
        }), 200

    else:
        return jsonify({"msg": "Error de autenticación en la API externa."}), 401


@auth_bp.route('/productos', methods=['GET'])
def get_productos():

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"msg": "Falta el token JWT en la cabecera"}), 401


    headers = {
        'Authorization': f'Bearer {token}'  
    }


    productos_response = requests.get(f"{API_URL}/getProductos", headers=headers)


    if productos_response.status_code == 200:
        productos_data = productos_response.json()  


        for producto in productos_data:

            existing_product = Product.query.filter_by(id=producto['PROId']).first()

            if existing_product:
    
                existing_product.quantity += 1
            else:

                new_product = Product(
                    id=producto['PROId'],
                    name=producto['PRODNombre'],
                    quantity=1,  
                    estado=producto['PRODEstado'],
                    fecha=producto['PRODFecha'],
                    imagen=producto['PRODImagen'],
                    precio=producto['PRODPrecio']
                )
                db.session.add(new_product)  


        db.session.commit()

        return jsonify({"msg": "Productos sincronizados correctamente"}), 200
    else:

        return jsonify({
            "msg": "Error al obtener los productos",
            "status_code": productos_response.status_code,
            "response": productos_response.text
        }), productos_response.status_code
