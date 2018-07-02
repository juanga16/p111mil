-- Usando la base de datos de personas, necesita saber/hacer. Escribir la sentencia SQL e informar el resultado.

-- 1) Mostrar todas las mujeres que vivan en Valencia o en Valladolid.
select *
from persona
where genero = 'F' and ciudad in ('Valencia', 'Valladolid');

-- 2) Mostrar el listado de las diez personas mas jovenes, ordenado del mas joven al mas viejo.
select *
from persona
order by fecha_nacimiento desc
limit 10;

-- 3) Mostrar las 5 personas de Madrid con mayor sueldo, pero en vez de mensual calcular el sueldo total de un año.
select *, sueldo * 12 as sueldo_anual
from persona
where ciudad = 'Madrid'
order by sueldo desc
limit 5;

-- 4) Mostrar las ciudades y cantidad de habitantes, ordenadas por cantidad descendente solamente si tienen mas de 10 personas.
select ciudad, count(*) as cantidad
from persona
group by ciudad
having cantidad > 10
order by cantidad desc;

-- 5) Mostrar todas las ciudades que tengan solamente una persona.
select ciudad
from persona
group by ciudad
having count(*) = 1
order by ciudad;

-- 6) Mostrar el año y la cantidad de personas de las mujeres de la tabla, ordenado por año descendente.
select year(fecha_nacimiento) as anio, count(*) as cantidad
from persona
where genero = 'F'
group by anio
order by anio desc;

-- 7) Mostrar el apellido mas repetido e informar la cantidad.
select apellido, count(*) as cantidad
from persona
group by apellido
order by cantidad
limit 1;

-- 8) Actualizar el apellido a 'Lopez' y la fecha de nacimiento a 17 de Junio de 1995 del registro con ID 560.
update persona
set apellido = 'Lopez',
	fecha_nacimiento = '1995-06-17'
where id = 560;    


-- 9) Aumentar el sueldo en un 3% de las personas que viven en Barcelona y aumentarlo en un 2% de las personas que viven en Valencia.
update persona
set sueldo = sueldo * 1.03
where ciudad = 'Barcelona';

update persona
set sueldo = sueldo * 1.02
where ciudad = 'Valencia';

-- 10) Insertar dos nuevos registros, la condicion es que todos los campos tengan valores.
insert into persona
(id, nombre, apellido, email, genero, ciudad, telefono, fecha_nacimiento, sueldo)
values
(100001, 'Diego', 'Velazquez', 'diego.velazquez@email.net', 'M', 'Lugo', '555-444-333', '1980-12-21', 20000),
(100002, 'Rosalia', 'Fernandez', 'rosalia_fernandez@email.net', 'F', 'La Coruña', '123-777-456', '1950-07-15', 21222.37);

-- 11) Informar el maximo sueldo de cada ciudad de los nacidos en el año 2000 ordenados por ciudad.
select ciudad, max(sueldo) as sueldo_maximo
from persona
where year(fecha_nacimiento) = 2000
group by ciudad;

-- 12) Informar el sueldo promedio de varones y de mujeres.
select genero, avg(sueldo) as sueldo_promedio
from persona
group by genero;

-- 13) Informar todas las personas que hayan nacido el dia de Navidad
select *
from persona
where day(fecha_nacimiento) = 25 and month(fecha_nacimiento) = 12;

-- 14) Listar solamente nombre y apellidos concatenados en una columna y los telefonos de las personas que viven en Sevilla
select concat(nombre, ' ', apellido) as nombre_apellido, telefono
from persona
where ciudad = 'Sevilla';

-- 15) Borrar el registro con id igual a 980
delete
from persona
where id = 980;