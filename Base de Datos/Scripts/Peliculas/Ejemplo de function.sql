delimiter $$

drop function if exists cantidadDePeliculasPorPais $$

create function cantidadDePeliculasPorPais (id_pais int) 
    returns int
begin
	declare cantidad int;
    
    select count(*)
    into cantidad
    from pelicula_pais pp
    where pp.id_pais = id_pais;
    
    return cantidad;
end
$$

select cantidadDePeliculasPorPais(6);