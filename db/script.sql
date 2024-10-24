CREATE DATABASE prueba;
USE prueba;

DROP DATABASE prueba;


select*from user;
select*from product;
select*from cart_item;
select*from purchase;
delete from product where PROId = 1;

-- Tabla de usuarios
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(80) NOT NULL,
    token VARCHAR(500) 
);

-- Tabla de productos
CREATE TABLE product (
    PROId INT AUTO_INCREMENT PRIMARY KEY,
    PRODNombre VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    PRODEstado BOOLEAN NOT NULL DEFAULT TRUE,  
    PRODFecha DATETIME NOT NULL, 
    PRODImagen VARCHAR(255),  
    PRODPrecio FLOAT NOT NULL  
);

-- Tabla del carrito de compras
CREATE TABLE cart_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    PROId INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (PROId) REFERENCES product(PROId),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Tabla de compras
CREATE TABLE purchase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (product_id) REFERENCES product(PROId)
);




