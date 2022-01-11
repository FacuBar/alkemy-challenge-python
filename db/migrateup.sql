CREATE TABLE `espacios_culturales` (
  `nombre`              VARCHAR(80)
  `web`                 VARCHAR(255)
  `mail`                VARCHAR(255)
  `domicilio`           VARCHAR(255)
  `id_departamento`     INT
  `localidad`           VARCHAR(255)
  `cod_localidad`       INT 
  `provincia`           VARCHAR(100)
  `id_provincia`        INT 
  `código_postal`       VARCHAR(8)
  `número_de_teléfono`  VARCHAR(15)
  `categoría`           VARCHAR(255)

  PRIMARY KEY (`nombre`, `provincia`)  
);

CREATE TABLE `cines_aggr_provincia` (
  `provincia`              VARCHAR(100)
  `cantidad_pantallas`     INT
  `cantidad_butacas`       INT
  `cantidad_espcios_incaa` INT

  PRIMARY KEY (`provincia`)
);

CREATE TABLE `registros_categoria` (
  `total`     INT
  `categoria` VARCHAR(255)   

  PRIMARY KEY (`categoria`)
);

CREATE TABLE `registros_fuente` (
  `total`   INT
  `fuente`  VARCHAR(255)

  PRIMARY KEY (`fuente`)
);

CREATE TABLE `registros_provincia_categoria` (
  `total`     INT
  `provincia` VARCHAR(100)
  `categoria` VARCHAR(255)

  PRIMARY KEY (`provincia`,`categoria`)
);
