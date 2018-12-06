/* Listar todos los articulos que pesen mas 
que 0.50 ordenados por Ciudad */
select *
from articulo
where peso > 0.50
order by ciudad;

/* Listar los articulos que son entregados por
proveedores de su misma ciudad */
select distinct a.*
from proveedor p
inner join envio e on e.id_proveedor = p.id_proveedor
inner join articulo a on e.id_articulo = a.id_articulo 
where p.ciudad = a.ciudad;

/* Listar los nombres de articulos y los nombres de 
sus proveedores ordenados por articulo */
select distinct a.descripcion, p.nombre
from proveedor p
inner join envio e on e.id_proveedor = p.id_proveedor
inner join articulo a on e.id_articulo = a.id_articulo 
order by a.descripcion;

/* Armar un ranking de proveedores segun la cantidad
total de articulos entregados */
select p.nombre, sum(e.cantidad), count(e.cantidad), max(e.cantidad)
from proveedor p
inner join envio e on e.id_proveedor = p.id_proveedor
inner join articulo a on e.id_articulo = a.id_articulo 
group by p.nombre
having sum(e.cantidad) >= 25
order by sum(e.cantidad) desc;

/* Listar todos los proveedores y el total de articulos entregados */
select p.nombre, sum(e.cantidad)
from proveedor p
left join envio e on e.id_proveedor = p.id_proveedor
group by p.nombre
order by p.nombre