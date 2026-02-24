-- Quitar la restricción de clave primaria
ALTER TABLE estudiantes_inscritos DROP CONSTRAINT IF EXISTS estudiantes_inscritos_pkey;
-- (Opcional) Puedes agregar una columna id autoincremental como nueva clave primaria
-- ALTER TABLE estudiantes_inscritos ADD COLUMN id SERIAL PRIMARY KEY;
