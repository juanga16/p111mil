/*
	ESTRUCTURA GENERAL:
    - UPDATE
    - SET
    - WHERE
*/

-- Actualizo el nombre a Juan Carlos del registro con id igual a 1
update persona
set nombre = 'Juan Carlos'
where id = 1;

-- Actualizo el la fecha de nacimiento del registro con id igual a 2
update persona
set fecha_nacimiento = '1990-12-21'
where id = 2;

-- Aumento el sueldo en un 10% de los empleados de Valencia
update persona
set sueldo = sueldo * 1.1
where ciudad = 'Valencia' and id = 465;

-- Actualizo la ciudad y el sueldo de todas las Maria Angeles
update persona
set ciudad = 'La Coruña',
	sueldo = 25000.12
where nombre = 'Maria Angeles';

select *
from persona
where nombre = 'Maria Angeles';

/* 
	SINO PONGO NADA EN EL WHERE SE VAN A ACTUALIZAR TODOS LOS REGISTROS
    UNA BUENA PRACTICA ES ANTES DE EJECUTAR UN UPDATE PROBAR LA SENTENCIA EN UN SELECT PARA NO ARRUINAR LOS REGISTROS
*/
