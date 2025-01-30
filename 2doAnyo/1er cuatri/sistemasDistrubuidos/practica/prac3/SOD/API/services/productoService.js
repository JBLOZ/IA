'use strict';

const Producto = require('../models/producto');

async function obtenerProductoPorId(id) {
    try {
        return await Producto.findById(id);
    } catch (err) {
        throw new Error(`Error al obtener el producto: ${err}`);
    }
}

async function crearProducto(datosProducto) {
    try {
        const producto = new Producto(datosProducto);
        return await producto.save();
    } catch (err) {
        throw new Error(`Error al crear el producto: ${err}`);
    }
}

async function actualizarProducto(id, datosProducto) {
    try {
        return await Producto.findByIdAndUpdate(id, datosProducto, { new: true });
    } catch (err) {
        throw new Error(`Error al actualizar el producto: ${err}`);
    }
}

async function obtenerProductos() {
    try {
        return await Producto.find();
    } catch (err) {
        throw new Error(`Error al obtener los productos: ${err}`);
    }
}

async function eliminarProducto(id) {
    try {
        return await Producto.findByIdAndDelete(id);
    } catch (err) {
        throw new Error(`Error al eliminar el producto: ${err}`);
    }
}

module.exports = {
    obtenerProductoPorId,
    crearProducto,
    actualizarProducto,
    obtenerProductos,
    eliminarProducto
};
