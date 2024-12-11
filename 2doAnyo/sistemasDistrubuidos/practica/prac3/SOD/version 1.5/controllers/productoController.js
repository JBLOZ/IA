'use strict';

const productoService = require('../services/productoService');

async function obtenerProductoPorId (req, res)  {
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
        res.status(500).send({ mensaje: `Error al salvar en la base de datos: ${err.message}` });
    }
};

function generarProductoAleatorio() {
    const nombres = ["Producto Alfa", "Producto Beta", "Producto Gamma", "Producto Holka", "Producto Delta"];
    const descripciones = [
      "Este es el producto A",
      "Este es el producto B",
      "Este es el producto C",
      "Este es el producto R",
      "Este es el producto Z"
    ];
    const categorias = ["Categoría 1", "Categoría 2", "Categoría 3", "Categoría 4", "Categoría 5"];
  
    return {
      nombre: nombres[Math.floor(Math.random() * nombres.length)],
      precio: parseFloat((Math.random() * (100 - 10) + 10).toFixed(2)), // Precio entre 10.00 y 100.00
      descripcion: descripciones[Math.floor(Math.random() * descripciones.length)],
      categoria: categorias[Math.floor(Math.random() * categorias.length)],
      stock: Math.floor(Math.random() * (500 - 1) + 1) // Stock entre 1 y 500
    };
  }


async function crearProductoAleatorio (req, res) {
    console.log('POST /api/productoAletorio');
    const productoAleatorio = generarProductoAleatorio();
    console.log(productoAleatorio);

    try {
        const productoStored = await productoService.crearProducto(productoAleatorio);
        res.status(200).send({ producto: productoStored });
    } catch (err) {
        res.status(500).send({ mensaje: `Error al salvar en la base de datos: ${err.message}` });
    }
};

async function actualizarProducto(req, res) {
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
};

async function obtenerProductos (req, res) {
    try {
        const productos = await productoService.obtenerProductos();
        res.status(200).send({ productos });
    } catch (err) {
        res.status(500).send({ mensaje: `Error al obtener los productos: ${err.message}` });
    }
};

async function eliminarProducto(req, res) {
    let productoId = req.params.id;
    try {
        const productoDeleted = await productoService.eliminarProducto(productoId);
        if (!productoDeleted) {
            return res.status(404).send({ mensaje: 'El producto no existe' });
        }
        res.status(200).send({ mensaje: 'Producto eliminado correctamente' });
    } catch (err) {
        res.status(500).send({ mensaje: `Error al eliminar el producto: ${err.message}` });
    }
};

module.exports = {
    obtenerProductoPorId,
    crearProducto,
    crearProductoAleatorio,
    actualizarProducto,
    obtenerProductos,
    eliminarProducto
};
