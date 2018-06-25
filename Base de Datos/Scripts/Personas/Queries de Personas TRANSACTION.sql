-- INICIO UNA NUEVA TRANSACTION
start transaction;
	
    update persona
    set sueldo = 50000
    where id = 1;

-- rollback;
commit;

/*
	ROLLBACK ES PARA DESHACER LA TRANSACCION
    COMMIT ES PARA CONFIRMAR LA TRANSACCION
*/

select *
from persona
where id = 1;

