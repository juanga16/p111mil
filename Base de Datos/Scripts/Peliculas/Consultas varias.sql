set @idPelicula = 0;

select @idPelicula := max(id)
from pelicula;

select *
from pelicula
where id = @idPelicula;

select *
from pelicula_genero
where id_pelicula = @idPelicula;

select *
from pelicula_pais
where id_pelicula = @idPelicula;

select *
from pelicula_actor
where id_pelicula = @idPelicula;