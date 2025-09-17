-- #############################################################################
-- #                            TABLAS DE CONFIGURACIÓN                          #
-- #############################################################################

-- Tabla para almacenar los usuarios del sistema y sus roles
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    hash_contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(50) DEFAULT 'usuario' NOT NULL,
    fecha_creacion TIMESTAMPTZ DEFAULT now()
);

-- Tabla para almacenar los precios de los diferentes tipos de combustible
CREATE TABLE precios_combustibles (
    id SERIAL PRIMARY KEY,
    tipo_combustible VARCHAR(50) UNIQUE NOT NULL,
    precio_por_litro NUMERIC(10, 2) NOT NULL,
    fecha_actualizacion TIMESTAMPTZ DEFAULT now()
);


-- #############################################################################
-- #                               TABLAS MAESTRAS                               #
-- #############################################################################

-- Tabla para almacenar la información de los agentes/empleados
CREATE TABLE agentes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo VARCHAR(100),
    dni VARCHAR(20) UNIQUE NOT NULL,
    categoria VARCHAR(50)
);

-- Tabla para almacenar la información de los vehículos
CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    patente VARCHAR(20) UNIQUE NOT NULL,
    consumo NUMERIC(5, 2), -- Consumo en L/100km
    combustible VARCHAR(50), -- Tipo de combustible (ej. 'Nafta', 'Diesel')
    condicion VARCHAR(50), -- Condición (ej. 'Oficial', 'Afectado')
    activo BOOLEAN DEFAULT true
);


-- #############################################################################
-- #                             TABLAS TRANSACCIONALES                          #
-- #############################################################################

-- Tabla principal para los expedientes de viaje
CREATE TABLE expedientes (
    id SERIAL PRIMARY KEY,
    numero_expediente VARCHAR(100) UNIQUE NOT NULL,
    vehiculo_id INTEGER REFERENCES vehiculos(id),
    origen VARCHAR(255) NOT NULL,
    fecha_salida TIMESTAMP NOT NULL,
    fecha_regreso TIMESTAMP NOT NULL,
    objetivo_viaje TEXT,
    distancia_total_km NUMERIC(10, 2),
    combustible_estimado_lts NUMERIC(10, 2),
    monto_combustible_calculado NUMERIC(12, 2),
    monto_viaticos_calculado NUMERIC(12, 2),
    monto_total_expediente NUMERIC(12, 2),
    estado VARCHAR(50), -- 'Anticipo', 'Recomposicion', 'Cerrado'
    creado_por_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    fecha_creacion TIMESTAMPTZ DEFAULT now()
);

-- Tabla intermedia para la relación muchos-a-muchos entre expedientes y agentes
CREATE TABLE expediente_agentes (
    expediente_id INTEGER NOT NULL REFERENCES expedientes(id) ON DELETE CASCADE,
    agente_id INTEGER NOT NULL REFERENCES agentes(id),
    dias_viatico_calculados NUMERIC(5, 2),
    monto_viatico_calculado NUMERIC(12, 2),
    PRIMARY KEY (expediente_id, agente_id) -- Clave primaria compuesta para evitar duplicados
);

-- Tabla para registrar los múltiples destinos de un expediente
CREATE TABLE expediente_destinos (
    id SERIAL PRIMARY KEY,
    expediente_id INTEGER NOT NULL REFERENCES expedientes(id) ON DELETE CASCADE,
    destino VARCHAR(255) NOT NULL,
    orden INTEGER -- Para secuenciar las paradas del viaje (1, 2, 3...)
);


-- #############################################################################
-- #                                    ÍNDICES                                  #
-- #############################################################################

-- Índices para mejorar el rendimiento de las consultas más frecuentes
CREATE INDEX idx_expedientes_creado_por ON expedientes(creado_por_usuario_id);
CREATE INDEX idx_expediente_agentes_agente_id ON expediente_agentes(agente_id);
CREATE INDEX idx_agentes_dni ON agentes(dni);
CREATE INDEX idx_vehiculos_patente ON vehiculos(patente);
