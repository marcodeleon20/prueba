import requests
from models import Product, db  

API_URL = "https://apiexamen.compuflashgt.com/api"
API_KEY = "62245354621022924456"
USER_ID = 1000
USER_PASSWORD = "!G4l3n0!"

def sync_products():

    login_data = {
        "apiKey": API_KEY,
        "usrId": USER_ID,
        "usrPassword": USER_PASSWORD
    }

    login_response = requests.post(f"{API_URL}/Login", json=login_data)

    if login_response.status_code == 200:
        print("Autenticación exitosa en el servicio REST externo.")
        
     
        productos_response = requests.get(f"{API_URL}/getProductos")
        
        if productos_response.status_code == 200:
            productos = productos_response.json()
            for product_data in productos:
                product = Product.query.filter_by(id=product_data['id']).first()
                
                if product:
                    product.quantity = product_data['quantity']
                    product.price = product_data['price']
                else:
                    new_product = Product(
                        id=product_data['id'],
                        name=product_data['name'],
                        quantity=product_data['quantity'],
                        price=product_data['price']
                    )
                    db.session.add(new_product)
            db.session.commit()
            print("Sincronización de productos completada.")
        else:
            print("Error obteniendo productos:", productos_response.status_code)
    else:
        print("Error de autenticación con el servicio REST externo:", login_response.status_code)
