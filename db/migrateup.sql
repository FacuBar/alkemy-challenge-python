CREATE TABLE espacios_culturales (
  nombre              VARCHAR(255),
  web                 VARCHAR(255),
  mail                VARCHAR(255),
  domicilio           VARCHAR(255),
  id_departamento     INT,
  localidad           VARCHAR(255),
  cod_localidad       INT,
  provincia           VARCHAR(100),
  id_provincia        INT,
  código_postal       VARCHAR(100),
  número_de_teléfono  VARCHAR(15),
  categoría           VARCHAR(255),
  fuente              VARCHAR(255),
  cargado_en          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cines_aggr_provincia (
  provincia       VARCHAR(255),
  pantallas       INT,
  butacas         INT,
  espacios_incaa  INT,
  cargado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registros_categoria (
  categoría   VARCHAR(255), 
  total       INT,
  cargado_en  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registros_fuente (
  fuente      VARCHAR(255),
  total       INT,
  cargado_en  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registros_provincia_categoria (
  provincia   VARCHAR(100),
  categoría   VARCHAR(255),
  total       INT,
  cargado_en  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
