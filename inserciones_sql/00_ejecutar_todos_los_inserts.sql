-- SCRIPT PARA EJECUTAR TODOS LOS INSERTS
-- ======================================

BEGIN TRANSACTION;

-- Optimizaciones para inserción masiva
ALTER TABLE estudiantes_inscritos DISABLE TRIGGER ALL;

-- Ejecutar: crear_tabla_estudiantes_inscritos.sql
\i crear_tabla_estudiantes_inscritos.sql

-- Ejecutar: inscripciones_2010_inserts.sql
\i inscripciones_2010_inserts.sql

-- Ejecutar: inscripciones_2011_inserts.sql
\i inscripciones_2011_inserts.sql

-- Ejecutar: inscripciones_2012_inserts.sql
\i inscripciones_2012_inserts.sql

-- Ejecutar: inscripciones_2013_inserts.sql
\i inscripciones_2013_inserts.sql

-- Ejecutar: inscripciones_2014_inserts.sql
\i inscripciones_2014_inserts.sql

-- Ejecutar: inscripciones_2016_inserts.sql
\i inscripciones_2016_inserts.sql

-- Ejecutar: inscripciones_2017_inserts.sql
\i inscripciones_2017_inserts.sql

-- Ejecutar: inscripciones_2018_inserts.sql
\i inscripciones_2018_inserts.sql

-- Ejecutar: inscripciones_2019_inserts.sql
\i inscripciones_2019_inserts.sql

-- Ejecutar: inscripciones_2020_inserts.sql
\i inscripciones_2020_inserts.sql

-- Ejecutar: inscripciones_2021_inserts.sql
\i inscripciones_2021_inserts.sql

-- Ejecutar: inscripciones_2023_inserts.sql
\i inscripciones_2023_inserts.sql

-- Ejecutar: inscripciones_2024_inserts.sql
\i inscripciones_2024_inserts.sql

-- Ejecutar: todos_los_inserts.sql
\i todos_los_inserts.sql

ALTER TABLE estudiantes_inscritos ENABLE TRIGGER ALL;

COMMIT;

-- FIN DEL SCRIPT
