create view detalle_pelicula as
	select p.titulo as pelicula, concat(a.nombre, ' ', a.apellido) as actor
    from pelicula p
    inner join pelicula_actor pa on pa.id_pelicula	= p.id
    inner join actor a on a.id = pa.id_actor;
    
select *
from detalle_pelicula;