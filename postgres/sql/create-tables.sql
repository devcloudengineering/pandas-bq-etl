CREATE TABLE clientes (
  cliente_id INTEGER PRIMARY KEY,
  rut VARCHAR(12),
  nombre VARCHAR(80),
  apellido VARCHAR(80),
  email VARCHAR(120),
  telefono VARCHAR(20),
  fecha_registro DATE,
  region VARCHAR(80),
  comuna VARCHAR(80),
  direccion VARCHAR(200),
  genero CHAR(1),
  fecha_nacimiento DATE
);

/* BQ clientes
CREATE TABLE `mi-primer-proyecto-469023.demo_hites.clientes` (
  cliente_id INTEGER,
  rut STRING(12),
  nombre STRING(80),
  apellido STRING(80),
  email STRING(120),
  telefono STRING(20),
  fecha_registro DATE,
  region STRING(80),
  comuna STRING(80),
  direccion STRING(200),
  genero STRING(1),
  fecha_nacimiento DATE
);
*/

CREATE TABLE productos (
  producto_id INTEGER PRIMARY KEY,
  sku VARCHAR(16) UNIQUE,
  nombre_producto VARCHAR(200),
  categoria VARCHAR(60),
  subcategoria VARCHAR(60),
  marca VARCHAR(60),
  precio_lista INTEGER,
  costo INTEGER,
  stock INTEGER,
  activo BOOLEAN,
  fecha_creacion DATE
);


/* BQ productos
CREATE TABLE `mi-primer-proyecto-469023.demo_hites.productos` (
  producto_id INTEGER,
  sku STRING(16),
  nombre_producto STRING(200),
  categoria STRING(60),
  subcategoria STRING(60),
  marca STRING(60),
  precio_lista INTEGER,
  costo INTEGER,
  stock INTEGER,
  activo BOOLEAN,
  fecha_creacion DATE
);
*/


CREATE TABLE ventas (
  venta_id INTEGER PRIMARY KEY,
  fecha_venta TIMESTAMP,
  cliente_id INTEGER REFERENCES clientes(cliente_id),
  producto_id INTEGER REFERENCES productos(producto_id),
  sku VARCHAR(16),
  canal VARCHAR(20),
  medio_pago VARCHAR(20),
  precio_unitario INTEGER,
  cantidad INTEGER,
  descuento_pct NUMERIC(4,2),
  subtotal INTEGER,
  impuesto_iva INTEGER,
  total_neto INTEGER,
  estado_pedido VARCHAR(20),
  metodo_envio VARCHAR(20),
  region_envio VARCHAR(80),
  comuna_envio VARCHAR(80),
  tienda_retiro VARCHAR(80)
);


/* BQ ventas
CREATE TABLE `mi-primer-proyecto-469023.demo_hites.ventas` (
  venta_id INTEGER,
  fecha_venta TIMESTAMP,
  cliente_id INTEGER,
  producto_id INTEGER,
  sku STRING(16),
  canal STRING(20),
  medio_pago STRING(20),
  precio_unitario INTEGER,
  cantidad INTEGER,
  descuento_pct NUMERIC(4,2),
  subtotal INTEGER,
  impuesto_iva INTEGER,
  total_neto INTEGER,
  estado_pedido STRING(20),
  metodo_envio STRING(20),
  region_envio STRING(80),
  comuna_envio STRING(80),
  tienda_retiro STRING(80)
);
*/
CREATE INDEX idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX idx_ventas_producto ON ventas(producto_id);


/*

OPERACIONES CON FECHAS BQ

SELECT PARSE_DATE('%Y/%m/%d', '2025/12/31') AS FECHA_CONVERTIDA;
SELECT CURRENT_DATE();
SELECT FORMAT_DATE('%d/%m/%Y', '2025-12-31');
SELECT DATE_ADD(PARSE_DATE('%Y/%m/%d', '2025/12/31'), INTERVAL 7 DAY) AS DATE_7_DIAS_MAS;
SELECT DATE_SUB(PARSE_DATE('%Y/%m/%d', '2025/12/31'), INTERVAL 7 DAY) AS DATE_7_DIAS_MENOS;

SELECT
  '2025-09-11' AS fecha_original,
  DATE_ADD(DATE '2025-09-11', INTERVAL 10 DAY) AS fecha_futura,
  DATE_SUB(DATE '2025-09-11', INTERVAL 1 YEAR) AS fecha_pasada,
  EXTRACT(MONTH FROM DATE '2025-09-11') AS mes,
  DATE_DIFF(DATE '2025-10-01', DATE '2025-09-11', DAY) AS dias_hasta_fin_mes,
  FORMAT_DATE('%A, %B %d, %Y', DATE '2025-09-11') AS fecha_formateada,
  DATE_TRUNC(DATE '2025-10-05', MONTH) AS fecha_primer_dia

*/