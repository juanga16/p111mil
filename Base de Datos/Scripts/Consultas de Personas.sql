/*
	TIPOS DE DATOS:
    https://dev.mysql.com/doc/refman/8.0/en/data-types.html
    
    INT(X): Numero entero de entre 1 y X digitos
    DECIMAL (X, Y): Numero de hasta X digitos (enteros y decimales) con Y decimales
    VARCHAR(X): Texto de hasta X caracteres
    CHAR (X): Texto de hasta X caracteres. Fijo, es decir, se ocupa el resto con espacios en blanco
    DATE: Fecha 'YYYY-MM-DD'
    DATETIME: Fecha y Hora 'YYYY-MM-DD HH:MM:SS'
    TIME: Hora 'HH:MM:SS'
    BIT: 0 o 1 el equivalente a BOOLEAN (1 seria TRUE)    
*/

-- Comentarios de una sola linea

/*
	Comentarios
    de multiples
    lineas
*/

-- Devuelve todas las columnas de todos los registros de la tabla Persona
select *
from persona;

--  Devuelve las columnas nombre y apellido de todos los registros
select nombre, apellido
from persona;

-- Selecciona todos los registros de todas las columnas y devuelve una unica fila por combinacion
select distinct nombre
from persona;

-- Selecciona todos los registros en los cuales el valor de genero sea 'Male'
select *
from persona
where genero = 'male';

-- Selecciona todas las personas cuyo nombre comienza con J
select *
from persona
where nombre like 'j%';

-- Selecciona todas las personas cuyo nombre termina con A
select *
from persona
where nombre like '%a';

-- Selecciona todas las personas cuyo nombre contiene NA
select *
from persona
where nombre like '%na%';

-- Selecciona el año, el mes y el dia de las fechas de nacimiento
select year(fecha_nacimiento), month(fecha_nacimiento), day(fecha_nacimiento)
from persona;

-- Selecciona el año, el mes y el dia de las fechas de nacimiento y luego aplica el operador distinct
select distinct year(fecha_nacimiento), month(fecha_nacimiento), day(fecha_nacimiento)
from persona;

-- Selecciona todas las personas con un sueldo mayor a 20000 y menor a 30000
select *
from persona
where sueldo between 20000 and 30000;

select *
from persona
where sueldo >= 20000 and sueldo <= 30000;

-- Selecciona todas las personas que nacieron entre el 1980-01-01 y el 1985-12-31 (la fecha se representa en formato Año-Mes-Dia)
select *
from persona
where fecha_nacimiento between '1980-01-01' and '1985-12-31';

select *
from persona
where fecha_nacimiento >= '1980-01-01' and fecha_nacimiento <= '1985-12-31';

-- Selecciona las primeras 5 personas que nacieron en 1990
select *
from persona
where year(fecha_nacimiento) = 1990
limit 5;

-- Selecciona todas las personas ordenadas por nombre y apellido
select *
from persona
order by nombre, apellido;

--  Selecciona todas las personas ordenadas por ciudad ascendente y luego por sueldo descendente
select *
from persona
order by ciudad, sueldo desc;

-- Selecciona las primeras 50 personas ordenadas por nombre y apellido
select *
from persona
order by nombre, apellido
limit 50;

-- Selecciona todas las personas que no viven en 'Philadelphia'
select *
from persona
where ciudad <> 'Philadelphia';

select *
from persona
where not ciudad = 'Philadelphia';

-- Selecciona todas las personas que viven en las siguientes ciudades: Philadelphia, Concepcion, Santa Rosa
select *
from persona
where ciudad in ('Philadelphia', 'Concepcion', 'Santa Rosa');

select *
from persona
where ciudad = 'Philadelphia' or ciudad = 'Concepcion' or ciudad = 'Santa Rosa';

-- Selecciona las primeras 10 personas que nacieron en 1990 o cuyo sueldo sea mayor que 30000
select *
from persona
where year(fecha_nacimiento) = 1990 or sueldo > 30000
limit 10;

-- Selecciona los registros entre la fila 50 y la 75
select *
from persona
limit 50, 25;