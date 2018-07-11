-- Seleccionar los nombres y apellidos de los clientes
SELECT 
    nombre, apellido
FROM
    e01_cliente;

-- Obtener todos los datos de todos los clientes.
SELECT 
    *
FROM
    e01_cliente;

-- Obtener las distintas marcas de los productos.
SELECT DISTINCT
    marca
FROM
    e01_producto;

-- Seleccionar los nombres y las marcas de los productos cuyo precio sea superior a 900$.
SELECT 
    nombre, marca
FROM
    e01_producto
WHERE
    precio > 900;    

-- Obtener la marca del producto cuyo código es 10.
SELECT 
    marca
FROM
    e01_producto
WHERE
    codigo_producto = 10;
    
-- Seleccionar código y nombre de los productos que tengan un stock de entre 60 y 100 unidades.
SELECT 
    codigo_producto, nombre
FROM
    e01_producto
WHERE
    stock BETWEEN 60 AND 90;

-- Seleccionar apellido y código del cliente con nombre “Jescie”.
SELECT 
    nro_cliente, apellido
FROM
    e01_cliente
WHERE
    nombre LIKE 'Jescie';
    
-- Seleccionar código, nombre y apellido de clientes cuyo nombre empiece con la letra “F”.
SELECT 
    nro_cliente, nombre, apellido
FROM
    e01_cliente
WHERE
    nombre LIKE 'F%';

-- Seleccionar código y nombre de los productos que tengan un stock de entre 60 y 90 unidades.
SELECT 
    codigo_producto, nombre
FROM
    e01_producto
WHERE
    stock >= 60 AND stock <= 90;

-- Obtener el código, nombre y stock de los productos cuyo nombre sea “fish” o tengan un stock de más de 26 unidades.
SELECT 
    codigo_producto, nombre, stock
FROM
    e01_producto
WHERE
    (nombre LIKE 'fish') OR (stock <= 26);
    
-- Obtener el número total de productos cuyo nombre es “fish”.
SELECT 
    COUNT(*)
FROM
    e01_producto
WHERE
    nombre LIKE 'fish';

-- Obtener el promedio del precio de los productos cuyo nombre es “fish”.
SELECT 
    AVG(precio)
FROM
    e01_producto
WHERE
    nombre LIKE 'fish';    
    
-- Seleccionar el nombre y el precio del producto más caro.
SELECT 
    nombre,MAX(precio)
FROM
    e01_producto;
    
-- Obtener el nombre y el precio del producto más barato.    
SELECT 
    nombre, MIN(precio)
FROM
    e01_producto;
       
-- Listar todos los productos junto con la cantidad que hay de cada uno.
SELECT 
    nombre, COUNT(codigo_producto)
FROM
    e01_producto
GROUP BY nombre;

-- Listar los datos de los clientes ordenados por apellido y nombre.
SELECT 
    *
FROM
    e01_cliente
ORDER BY apellido , nombre ASC;

-- Listar los primeros 3 productos más caros.
SELECT 
    *
FROM
    e01_producto
ORDER BY precio DESC
LIMIT 3;

-- Obtener el teléfono y el número de cliente del cliente con nombre “Wanda” y apellido “Baker”.
SELECT 
    *
FROM
    e01_telefono
WHERE
    nro_cliente IN (SELECT 
            nro_cliente
        FROM
            e01_cliente
        WHERE
            nombre LIKE 'Wanda'
                AND apellido LIKE 'Baker');

-- Seleccionar los datos de los clientes junto con sus teléfonos. 
SELECT 
    nombre, apellido, nro_telefono AS telefono
FROM
    e01_cliente c
        INNER JOIN
    e01_telefono t ON c.nro_cliente = t.nro_cliente;

-- Insertar en un nuevo teléfono del cliente número 50.
INSERT INTO `E01_TELEFONO` VALUES (229,4639675,'M',50);
INSERT INTO `E01_TELEFONO`(`nro_telefono`,`tipo`,`codigo_area`,`nro_cliente`) VALUES (4547894,'M',249,50);

-- Cambiar el nombre del cliente número 15 por "Juan"
UPDATE e01_cliente 
SET 
    nombre = 'Juan'
WHERE
    nro_cliente = 15;

-- Borrar todos los teléfonos del cliente número “20”.
DELETE FROM e01_telefono 
WHERE
    nro_cliente = 20;
