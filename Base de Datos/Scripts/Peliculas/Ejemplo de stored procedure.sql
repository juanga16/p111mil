delimiter //

drop procedure if exists peliculasPorPais //

create procedure peliculasPorPais()
begin
	select p.nombre as pais, count(*) as cantidadPeliculas
    from pais p
    inner join peliculaPais pp on pp.id_pais = p.id
    group by p.nombre;
end 
//

call peliculasPorPais();