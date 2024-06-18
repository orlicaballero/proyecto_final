CREATE TABLE criptomonedas (
    id VARCHAR(50),
    nombre VARCHAR(255),
    simbolo VARCHAR(10),
    precio_usd DECIMAL(18, 2),
    capitalizacion_usd DECIMAL(18, 2),
    volumen_24h_usd DECIMAL(18, 2),
    variacion_24h DECIMAL(5, 2),
    fecha_ingesta TIMESTAMP,
    PRIMARY KEY (id, fecha_ingesta)
);
