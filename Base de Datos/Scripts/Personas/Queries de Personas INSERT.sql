select *
from persona;

insert into persona
(id, nombre, apellido, email, genero, ciudad, telefono, fecha_nacimiento, sueldo)
values
(1001, 'José Luis', 'Torrente', 'jose@torrente.es', 'Masculino', 'Madrid', '960-760-769', '1965-07-17', 10000);

select *
from persona
where id >= 1001;

-- Si intento insertar otra persona con el mismo ID, da error
insert into persona
(id, nombre, apellido, email, genero, ciudad, telefono, fecha_nacimiento, sueldo)
values
(1001, 'Fernando', 'Torres', 'elniño@aleti.es', 'Masculino', 'Madrid', '960-760-769', '1984-03-20', 10000);

-- Inserto una persona solamente con el Id y con el Nombre
insert into persona
(id, nombre)
values
(1002, 'Juan')
 