from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes.auth_routes import auth_bp  # Importar el Blueprint de autenticación
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.report_routes import report_bp
from flask_cors import CORS  # Importar Flask-CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix='/auth')  
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(report_bp, url_prefix='/report')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


