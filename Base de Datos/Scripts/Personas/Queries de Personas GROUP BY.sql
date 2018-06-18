/*
	ESTRUCTURA GENERAL:
    - SELECT
    - FROM
    - GROUP BY
    - HAVING
    - ORDER BY
*/

-- Selecciono el mayor, el menor y el promedio de Sueldo
select MAX(sueldo), MIN(sueldo), AVG(sueldo)
from persona;

-- Selecciono el mayor y la menor Fecha de Nacimiento
select MAX(fecha_nacimiento), MIN(fecha_nacimiento), AVG(fecha_nacimiento)
from persona;

-- Selecciono la cantidad de registros
select COUNT(*)
from persona;

-- Agrupo los registros por ciudad, calculo la cantidad por ciudad y ordeno descendentemente por cantidad
select ciudad, COUNT(*)
from persona
group by ciudad
order by COUNT(*) desc;

-- Agrupo los registros por ciudad y calculo el promedio de sueldo
select ciudad, AVG(sueldo)
from persona
group by ciudad;

-- Agrupo los registros por genero y calculo la cantidad de la ciudad de Madrid
select genero, COUNT(*)
from persona
where ciudad = 'Madrid'
group by genero;


-- Agrupo los registros por ciudad y calculo el promedio de Sueldo de aquellas ciudades con mas de 10 registros
select ciudad, AVG(sueldo)
from persona
group by ciudad
having count(*) > 10
order by ciudad;

-- Dentro del Having y del Order By pueden ir o: columnas que esten en el Select o funciones de agregacion: COUNT, AVG, MAX y MIN
