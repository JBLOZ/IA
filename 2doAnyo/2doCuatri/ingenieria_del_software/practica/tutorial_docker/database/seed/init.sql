-- Crear la base de datos
USE tienda;

-- Tabla de Usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

-- Tabla de Pedidos (relación entre Usuarios y Productos)
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Insertar datos en Usuarios
INSERT INTO users (nombre, email) VALUES 
('Juan Pérez', 'juan@example.com'),
('Ana Gómez', 'ana@example.com'),
('Carlos Ruiz', 'carlos@example.com');

-- Insertar datos en Productos
INSERT INTO products (nombre, descripcion, precio, stock) VALUES 
('Laptop', 'Laptop de última generación', 1200.00, 10),
('Smartphone', 'Teléfono inteligente con gran cámara', 800.00, 15),
('Auriculares', 'Auriculares con cancelación de ruido', 150.00, 30);

-- Insertar datos en Pedidos
INSERT INTO orders (user_id, product_id, cantidad) VALUES 
(1, 1, 1),  -- Juan compra 1 Laptop
(2, 2, 2),  -- Ana compra 2 Smartphones
(3, 3, 1),  -- Carlos compra 1 Auricular
(1, 3, 3);  -- Juan compra 3 Auriculares