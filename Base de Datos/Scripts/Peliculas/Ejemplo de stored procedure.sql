delimiter //

drop procedure if exists peliculasPorPais //

create procedure peliculasPorPais()
begin
	select p.nombre as pais, count(*) as cantidad_peliculas
    from pais p
    inner join pelicula_pais pp on pp.id_pais = p.id
    group by p.nombre;
end 
//

call peliculasPorPais();