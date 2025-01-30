// index.js
'use strict';
const express = require('express');
const mongoose = require('mongoose');
const productoController = require('./controllers/productoController'); // Importar el controlador
const app = express();
const PORT = 8080;
// Conectar a MongoDB
mongoose.connect('mongodb://localhost:27017/producto')
.then(() => {
console.log('Conexión a la base de datos establecida');
}).catch(err => {
console.error('Error de conexión a la base de datos:', err);
});
app.use(express.json());
// Definir las rutas y asignarles los métodos del controlador
app.get('/api/producto/:id', productoController.obtenerProductoPorId);
app.post('/api/producto', productoController.crearProducto);
app.listen(PORT, () => {
console.log(`API REST ejecutándose en http://localhost:${PORT}`);
});
