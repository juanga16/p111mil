start transaction;
	
    update persona
    set sueldo = 50000
    where id = 1;

-- rollback;
commit;

select *
from persona
where id = 1;

