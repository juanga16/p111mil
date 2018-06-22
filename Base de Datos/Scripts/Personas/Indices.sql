select count(*)
from persona;

select *
from persona
where id = 75000;

select *
from persona
where nombre = 'Juan';

alter table persona
add index ix_nombre (nombre asc);

alter table persona
drop index ix_nombre;