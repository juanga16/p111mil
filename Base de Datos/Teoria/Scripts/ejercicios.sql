-- Primer set de ejercicios

-- 1. Obtener todos los datos de todos los clientes.
SELECT 
    *
FROM
    e01_cliente;

-- 2. Obtener solo los nombres y apellidos de todos los clientes.
SELECT 
    nombre, apellido
FROM
    e01_cliente;

-- 3. Obtener los nombres nombres de los diferentes productos que se venden.
SELECT DISTINCT
    nombre
FROM
    e01_producto;

-- 4. Obtener los diferentes códigos de área de los teléfonos.
SELECT DISTINCT
    codigo_area
FROM
    e01_telefono;

-- Segundo set de ejercicios

-- 1. Obtener el listado de todos los productos que tengan un stock mayor a 50 y menor a 200.
SELECT 
    codigo_producto, nombre
FROM
    e01_producto
WHERE
    stock BETWEEN 50 AND 200;
    
-- 2. Obtener los datos correspondientes al producto cuyo codigo es 50.
SELECT 
    *
FROM
    e01_producto
WHERE
    codigo_producto = 50;

-- 3. Obtener los datos de las facturas cuyo total (con iva incluido) sea mayor a 400.000$ y lo haya realizado el cliente número 8. sea mayor a y lo haya realizado el cliente número tanto.
SELECT 
    *
FROM
    e01_factura
WHERE
    total_con_iva > 400000
        AND nro_cliente = 8;
        
-- 4. Obtener los datos del cliente cuyo nombre es “Ivor” y el apellido “Saunders”.
SELECT 
    *
FROM
    e01_cliente
WHERE
    nombre LIKE 'Ivor'
        AND apellido LIKE 'Saunders';

-- 5. Todas las Facturas pertenecientes al cliente número 10.
SELECT 
    *
FROM
    e01_factura
WHERE
    nro_cliente = 10;
    
-- 6. Todas las Facturas que superen los 500.000$.
SELECT 
    *
FROM
    e01_factura
WHERE
    total_con_iva > 500000;

-- Tercer set de ejercicios

-- 1. Obtener el número total de clientes que se encuentran registrados en la base de datos.
SELECT 
    COUNT(nro_cliente)
FROM
    e01_cliente;
    
-- 2. Listar el precio promedio de cada marca.
SELECT 
    marca, AVG(precio)
FROM
    e01_producto
GROUP BY marca;

-- 3. Listar el nombre junto con el precio promedio de los 10 primeros productos ordenados alfabéticamente.
SELECT 
    nombre, AVG(precio)
FROM
    e01_producto
GROUP BY nombre
ORDER BY nombre
LIMIT 10; 

-- 4. Listar lo que gastó cada cliente, mostrando el número de cliente y la suma total.
SELECT 
    nro_cliente, SUM(total_con_iva), SUM(total_sin_iva)
FROM
    e01_factura
GROUP BY nro_cliente;

-- 5. Listar las marcas cuyo promedio de precios sea mayor a 600$.
SELECT 
    marca, AVG(precio)
FROM
    e01_producto
GROUP BY marca
HAVING AVG(precio) > 600;

-- Cuarto set de ejercicios

-- 1. Listar todas las Facturas que hayan sido compradas por el cliente de nombre "Pandora" y apellido "Tate".
SELECT 
    *
FROM
    e01_factura
WHERE
    nro_cliente IN (SELECT 
            nro_cliente
        FROM
            e01_cliente
        WHERE
            nombre LIKE 'Pandora'
                AND apellido LIKE 'Tate');

-- 2. Listar todas las Facturas que contengan productos de la marca "In Faucibus Inc.".
SELECT 
    *
FROM
    e01_factura
WHERE
    nro_factura IN (SELECT 
            nro_factura
        FROM
            e01_detalle_factura
        WHERE
            codigo_producto IN (SELECT 
                    codigo_producto
                FROM
                    e01_producto
                WHERE
                    marca LIKE 'In Faucibus Inc.'));
            
-- Quinto set de ejercicios

-- 1. Mostrar cada teléfono junto con los datos del cliente.
SELECT 
    c.*, t.*
FROM
    e01_cliente c
        INNER JOIN
    e01_telefono t ON (c.nro_cliente = t.nro_cliente);

-- 2. Mostrar todos los teléfonos del cliente número 30 junto con todos sus datos personales.
SELECT 
    c.*, t.*
FROM
    e01_cliente c
        INNER JOIN
    e01_telefono t ON (c.nro_cliente = t.nro_cliente)
WHERE
    c.nro_cliente = 30;

-- 3. Mostrar nombre y apellido de cada cliente junto con lo que gastó en total (con iva incluido).
SELECT 
    c.nombre,
    c.apellido,
    SUM(f.total_con_iva),
    SUM(f.total_sin_iva)
FROM
    e01_cliente c
        INNER JOIN
    e01_factura f ON (c.nro_cliente = f.nro_cliente)
GROUP BY c.nro_cliente;

-- Sexto set de ejercicios

-- Insertar el producto "turron" de la empresa "misky" con un precio de 4$ y un stock de 100 unidades.
INSERT INTO e01_producto(codigo_producto,marca,nombre,descripcion,precio,stock) VALUES (102,"Misky","turron","turron de mani","4",100);

-- Actualizar el codigo de area por "526" de los telefonos que tenían código de área "551"
UPDATE e01_telefono 
SET 
    codigo_area = 526
WHERE
    codigo_area = 551;
    

-- Borrar el producto insertado en 1
DELETE FROM e01_producto 
WHERE
    nombre = 'turron' AND marca = 'misky';