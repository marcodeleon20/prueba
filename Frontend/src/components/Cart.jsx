import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { AppBar, Toolbar, Typography, Button, Container, Grid, Card, CardContent, Divider } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const token = localStorage.getItem('token');  
  const userId = localStorage.getItem('userId');  

  useEffect(() => {

    fetchCartItems();
  }, [token, userId]);

 
  const fetchCartItems = () => {
    axios
      .get(`http://34.56.73.111:5000/cart/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          user_id: userId,
        },
      })
      .then((response) => {
        setCartItems(response.data);  
      })
      .catch((error) => {
        console.error('Error al obtener el carrito:', error);
      });
  };


  const confirmPurchase = () => {
    axios
      .post(
        'http://34.56.73.111:5000/cart/confirm',
        { user_id: userId },  
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((response) => {
        alert('Compra confirmada con éxito');
    
        window.location.reload();  
      })
      .catch((error) => {
        console.error('Error al confirmar la compra:', error);
      });
  };

  return (
    <div>
      {/* Navbar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Mi Tienda
          </Typography>
          <Button color="inherit" href="/">
            Productos
          </Button>
          <Button color="inherit" startIcon={<ShoppingCartIcon />} href="/cart">
            Carrito
          </Button>
        </Toolbar>
      </AppBar>

      {/* Contenido del carrito */}
      <Container maxWidth="md" sx={{ marginTop: 4 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Carrito de Compras
        </Typography>

        {cartItems.length > 0 ? (
          <Grid container spacing={3}>
            {cartItems.map((item) => (
              <Grid item xs={12} key={item.product_id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{item.name}</Typography>
                    <Typography variant="body1">Precio: Q{item.price.toFixed(2)}</Typography>
                    <Typography variant="body1">Cantidad: {item.quantity}</Typography>
                    <Typography variant="body1">Total: Q{item.total.toFixed(2)}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Button
                variant="contained"
                color="primary"
                onClick={confirmPurchase}
                fullWidth
              >
                Confirmar Compra
              </Button>
            </Grid>
          </Grid>
        ) : (
          <Typography variant="body1" align="center">
            El carrito está vacío.
          </Typography>
        )}
      </Container>
    </div>
  );
};

export default Cart;
