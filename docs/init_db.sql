-- =========================================================
-- SCRIPT INICIALIZADOR DE BASE DE DATOS PARA GLOWY
-- Tienda de Skincare Coreano
-- Autor: [Tu nombre]
-- Fecha: 2026-02-03
-- Descripción:
--   Este script elimina la base de datos si ya existe,
--   la vuelve a crear desde cero y define la tabla 'productos'.
-- =========================================================

-- 1️⃣ Borrar la base de datos si ya existe
DROP DATABASE IF EXISTS glowy_db;

-- 2️⃣ Crear una nueva base de datos
CREATE DATABASE glowy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- 3️⃣ Seleccionar la base de datos recién creada
USE glowy_db;

-- 4️⃣ Crear tabla 'productos'
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    descripcion TEXT
);

-- 5️⃣ Insertar algunos productos de ejemplo
INSERT INTO productos (nombre, categoria, precio, stock, descripcion) VALUES
('COSRX Snail Mucin 96 Power Essence', 'Serum', 24.99, 50, 'Esencia con 96% de mucina de caracol para hidratar y reparar la piel'),
('Laneige Water Sleeping Mask', 'Moisturizer', 35.00, 30, 'Mascarilla nocturna que hidrata profundamente mientras duermes'),
('Beauty of Joseon Dynasty Cream', 'Moisturizer', 22.50, 40, 'Crema nutritiva con ingredientes tradicionales coreanos'),
('Innisfree Green Tea Cleansing Foam', 'Cleanser', 12.99, 60, 'Espuma limpiadora con extracto de té verde de Jeju'),
('Missha Time Revolution Night Repair', 'Serum', 48.00, 25, 'Serum antiedad con tecnología de fermentación'),
('Etude House Sunprise Mild Watery Light', 'Sunscreen', 15.99, 45, 'Protector solar SPF50+ con textura acuosa ligera'),
('Dear Klairs Supple Preparation Toner', 'Toner', 19.99, 35, 'Tónico equilibrante libre de alcohol para todo tipo de piel'),
('Some By Mi AHA BHA PHA 30 Days Miracle Toner', 'Toner', 18.50, 42, 'Tónico exfoliante con triple ácido para mejorar textura');

-- 6️⃣ Confirmar
SELECT * FROM productos;
