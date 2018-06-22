delimiter //

drop trigger if exists pais_fecha_creation //

create trigger pais_fecha_creation
	before insert on pais
    for each row
begin
	set new.fecha_creacion = now();
end //

insert into pais
(nombre)
values
('Italia');

select *
from pais;