from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Modelo para la tabla de usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(500))  

# Modelo para la tabla de productos
class Product(db.Model):
    id = db.Column('PROId', db.Integer, primary_key=True)  # Campo PROId
    name = db.Column('PRODNombre', db.String(100), nullable=False)  # Campo PRODNombre
    quantity = db.Column(db.Integer, nullable=False)
    estado = db.Column('PRODEstado', db.Boolean, default=True)  # Campo PRODEstado
    fecha = db.Column('PRODFecha', db.DateTime, default=datetime.utcnow)  # Campo PRODFecha
    imagen = db.Column('PRODImagen', db.String(255))  # Campo PRODImagen
    precio = db.Column('PRODPrecio', db.Float, nullable=False)  # Campo PRODPrecio

# Modelo para la tabla del carrito de compras
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column('PROId', db.Integer, db.ForeignKey('product.PROId'), nullable=False)  # Referencia a PROId
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Modelo para la tabla de compras
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.PROId'), nullable=False)  # Referencia correcta a PROId
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
