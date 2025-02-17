'use strict';

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const productoController = require('./controllers/productoController');
const app = express();
const PORT = 8080;

// Conectar a MongoDB
mongoose.connect('mongodb://localhost:27017/producto')
  .then(() => {
    console.log('Conexión a la base de datos establecida');
  })
  .catch(err => {
    console.error('Error de conexión a la base de datos:', err);
  });

app.use(express.json());

// Habilitar CORS
app.use(cors());

// Rutas
app.get('/api/producto', productoController.obtenerProductos);
app.get('/api/producto/:id', productoController.obtenerProductoPorId);
app.post('/api/producto', productoController.crearProducto);
app.post('/api/productoaleatorio', productoController.crearProductoAleatorio);
app.put('/api/producto/:id', productoController.actualizarProducto);
app.delete('/api/producto/:id', productoController.eliminarProducto);

app.listen(PORT, () => {
  console.log(`API REST ejecutándose en http://localhost:${PORT}`);
});
