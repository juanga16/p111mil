-- Todas las peliculas y todos los actores
select p.titulo, a.nombre, a.apellido
from pelicula p
inner join peliculaActor pa on pa.id_pelicula = p.id
inner join actor a on a.id = pa.id_actor;

-- Todos los actores de El secreto de sus ojos
select *
from actor a
inner join peliculaActor pa on pa.id_actor = a.id
where pa.id_pelicula = 1;

select a.*
from actor a
inner join peliculaActor pa on pa.id_actor = a.id
inner join pelicula p on p.id = pa.id_pelicula
where p.titulo= 'El secreto de sus ojos';

select a.*
from actor a
inner join peliculaActor pa on pa.id_actor = a.id
where pa.id_pelicula in (select p.id
						 from pelicula p
						 where p.titulo = 'El secreto de sus ojos');

-- cantidad de peliculas por director
select d.*, count(*)
from director d
inner join pelicula p on p.id_director = p.id
group by d.id
order by count(*) desc

/*
	Escribir las queries para obtener:
    
	- Las peliculas en las que actuó Soledad Villamil
    - Todos los generos de peliculas que dirigio Juan Jose Campanela
    - Las peliculas ordenadas por ranking
    - La pelicula con mayor puntuacion
    - Una funcion que devuelva el promedio de edad (en años) de los protagonistas de una pelicula
    - Un stored procedure que devuelva el listado de peliculas y sus generos
*/

                         