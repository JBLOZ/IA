// controllers/productoController.js
'use strict';
const productoService = require('../services/productoService');
async function obtenerProductoPorId (req, res) {
let productoId = req.params.id;
try {
const producto = await productoService.obtenerProductoPorId(productoId);
if (!producto) {
return res.status(404).send({ mensaje: 'El producto no existe' });
}
res.status(200).send({ producto });
} catch (err) {
res.status(500).send({ mensaje: `Error al realizar la petición: ${err.message}` });
}
};
async function crearProducto (req, res) {
console.log('POST /api/producto');
console.log(req.body);
try {
const productoStored = await productoService.crearProducto(req.body);
res.status(200).send({ producto: productoStored });
} catch (err) {
res.status(500).send({ mensaje: `Error al salvar en la base de datos: ${err.message}`
});
}
};
async function actualizarProducto(id, datosProducto) {
console.log('PUT /api/producto/:id');
console.log(req.body);
let productoId = req.params.id;
let update = req.body;
try {
const productoUpdated = await productoService.actualizarProducto(productoId, update);
if (!productoUpdated) {
return res.status(404).send({ mensaje: 'El producto no existe' });
}
res.status(200).send({ producto: productoUpdated });
} catch (err) {
res.status(500).send({ mensaje: `Error al actualizar el producto: ${err.message}` });
}
}

module.exports = {
    obtenerProductoPorId,
    crearProducto,
    actualizarProducto
    };
