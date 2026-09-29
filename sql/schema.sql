-- =============================================================
-- SECCIÓN 2.1: Modelado de Datos (DDL)
-- =============================================================
-- Instrucciones:
-- Escribe las sentencias CREATE TABLE para almacenar 'desarrollos' y 'leads'.
-- Considera llaves primarias, foráneas, tipos de datos e índices recomendados.

-- CREATE TABLE desarrollos (...);

-- CREATE TABLE leads (...);

CREATE TABLE desarrollos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    ciudad VARCHAR(100),
    estado VARCHAR(100)
);

CREATE TABLE leads(
    id INT PRIMARY KEY ,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    origen VARCHAR(50) NOT NULL,
    campaña VARCHAR(50) NOT NULL,
    fecha_registro DATETIME NOT NULL,
    estatus ENUM('NUEVO','CONTACTADO','EN_SEGUIMIENTO','CONVERTIDO','PERDIDO') NOT NULL DEFAULT 'NUEVO',
    presupuesto decimal(10,2) NOT NULL,
    desarrollo_id INT NOT NULL,
    comentarios TEXT NOT NULL,
    FOREIGN KEY (desarrollo_id) REFERENCES desarrollos(id)
);