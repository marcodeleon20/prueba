import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Box, Typography, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';  // Importar el hook de navegación

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();  // Hook de React Router para redirigir

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://34.56.73.111:5000/auth/login', {
        usrId: username,
        usrPassword: password,
      });


      if (response.data.response_data.Token && response.data.usuario) {
        localStorage.setItem('token', response.data.response_data.Token);


        localStorage.setItem('userId', response.data.usuario.id);
        localStorage.setItem('username', response.data.usuario.username);
        console.log(response.data.response_data.Token)
        console.log(response.data.usuario.id)
        console.log(response.data.usuario.username)
        setMessage('Inicio de sesión exitoso');


        navigate('/');
      } else {
        setMessage('Error al iniciar sesión');
      }
    } catch (error) {
      setMessage('Error: ' + error.response?.data?.msg || 'Error en la solicitud');
    }
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: 4,
          boxShadow: 3,
          borderRadius: 2,
          backgroundColor: 'white',
        }}
      >
        <Typography component="h1" variant="h5" gutterBottom>
          Iniciar Sesión
        </Typography>
        <form onSubmit={handleLogin} style={{ width: '100%', marginTop: 1 }}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            label="Usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            label="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 2, mb: 2 }}
          >
            Iniciar Sesión
          </Button>
        </form>
        {message && (
          <Alert severity="info" sx={{ mt: 2 }}>
            {message}
          </Alert>
        )}
      </Box>
    </Container>
  );
};

export default Login;
