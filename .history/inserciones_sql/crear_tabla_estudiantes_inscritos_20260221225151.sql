CREATE TABLE estudiantes_inscritos (
    correlativo_estudiante VARCHAR(64) PRIMARY KEY,
    nombre_carrera VARCHAR(128),
    fecha_inscripcion DATE,
    anio_inscripcion INTEGER,
    sexo VARCHAR(8),
    pais_nacionalidad VARCHAR(64),
    tipo_inscripcion VARCHAR(64)
);
