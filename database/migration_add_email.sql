-- Migración: Agregar campo email a tabla usuarios
-- Fecha: 2025-09-02
-- Descripción: Agregar campo email a la tabla usuarios y migrar datos existentes

-- 1. Agregar nueva columna email
ALTER TABLE usuarios ADD COLUMN email VARCHAR(255);

-- 2. Migrar datos existentes: usar nombre_usuario como email temporal
UPDATE usuarios SET email = nombre_usuario WHERE email IS NULL;

-- 3. Crear índice único para email
CREATE UNIQUE INDEX idx_usuarios_email ON usuarios(email);

-- 4. Agregar constraint NOT NULL después de migrar datos
ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL;

-- Comentarios:
-- - Se mantiene nombre_usuario para retrocompatibilidad
-- - Se usa nombre_usuario como email temporal para usuarios existentes
-- - Se permite que los usuarios actualicen su email más tarde si es necesario
-- - El campo email tendrá validación adicional en el nivel de aplicación