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
    const nombres = [
        // Electrónica
        "Smartphone Samsung Galaxy S21", "Auriculares Bluetooth Sony WH-1000XM5", 
        "Laptop Dell XPS 13", "Tablet Apple iPad Air", "Monitor LG UltraFine 5K", 
        "Cámara Canon EOS Rebel T7", "Teclado Mecánico Razer BlackWidow", 
        "Reloj Inteligente Garmin Forerunner 945", "Barra de Sonido Bose Smart Soundbar 700", 
        "Disco Duro Externo WD 5TB",
        
        // Hogar
        "Aspiradora Dyson V11", "Cafetera Nespresso Vertuo Plus", "Robot Aspirador Roomba i7+", 
        "Ventilador de Torre Xiaomi SmartMi", "Hervidor de Agua Russell Hobbs", 
        "Batidora de Mano Braun MQ5000", "Juego de Ollas Tefal Ingenio", 
        "Sofá Modular IKEA KIVIK", "Colchón Viscoelástico Emma", 
        "Purificador de Aire Philips Series 3000",

        // Deportes
        "Bicicleta de Montaña Trek Marlin 7", "Balón de Fútbol Adidas Predator", 
        "Cinta de Correr NordicTrack Commercial 1750", "Set de Pesas Bowflex SelectTech", 
        "Patinete Eléctrico Xiaomi Mi Electric Scooter", "Casco de Ciclismo Giro Aether", 
        "Zapatillas de Running Nike Air Zoom Pegasus", "Palo de Golf Callaway Mavrik", 
        "Saco de Boxeo Everlast Powercore", "Reloj Deportivo Suunto 9 Baro",

        // Tecnología
        "Placa Base ASUS ROG Strix Z690", "Procesador Intel Core i9-12900K", 
        "Tarjeta Gráfica NVIDIA GeForce RTX 3080", "Memoria RAM Corsair Vengeance 32GB", 
        "SSD Samsung 970 EVO Plus 1TB", "Micrófono Blue Yeti X", 
        "Router WiFi 6 TP-Link Archer AX6000", "Impresora Láser HP Color Pro MFP", 
        "Cámara Web Logitech StreamCam", "Lector de Libros Electrónicos Kindle Paperwhite",

        // Alimentos
        "Pack de Café Molido Illy", "Caja de Té Verde Lipton", 
        "Botella de Vino Rioja Marqués de Riscal", "Aceite de Oliva Virgen Extra Carbonell", 
        "Chocolate Negro Lindt Excellence 70%", "Pack de Agua Mineral Evian", 
        "Bolsa de Frutos Secos Alesto", "Mermelada de Fresa Hero Premium", 
        "Arroz Integral SOS", "Cereal Nestlé Fitness Original"
    ];

    const descripciones = [
        "Última tecnología y alto rendimiento.",
        "Producto recomendado para un estilo de vida moderno.",
        "Diseño elegante y materiales duraderos.",
        "Ideal para uso en el hogar o la oficina.",
        "Altamente eficiente y fácil de usar.",
        "Producto premium con excelentes opiniones.",
        "Perfecto para quienes buscan calidad y confort.",
        "Diseñado para maximizar la productividad.",
        "Una solución versátil y práctica.",
        "Alta calidad a un precio accesible."
    ];

    const categorias = [
        "Electrónica", "Hogar", "Deportes", "Tecnología", "Alimentos", 
        "Moda", "Juguetes", "Libros", "Automoción", "Salud"
    ];

    return {
        nombre: nombres[Math.floor(Math.random() * nombres.length)],
        precio: parseFloat((Math.random() * (500 - 5) + 5).toFixed(2)), // Precio entre 5.00 y 500.00
        descripcion: descripciones[Math.floor(Math.random() * descripciones.length)],
        categoria: categorias[Math.floor(Math.random() * categorias.length)],
        stock: Math.floor(Math.random() * (1000 - 10) + 10) // Stock entre 10 y 1000
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
