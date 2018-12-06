insert into proveedor
(nombre, rubro, ciudad)
values
('Proveedor X', 'Limpieza', 'Coronel Suarez'),
('Proveedor Y', 'Higiene', 'Tandil'),
('Proveedor Z', 'Farmacia', 'Bolivar'),
('Proveedor W', 'Limpieza', 'Mar del Plata');

insert into articulo
(descripcion, peso, ciudad)
values
('Articulo A', 1.25, 'Coronel Suarez'),
('Articulo B', 0.95, 'Coronel Suarez'),
('Articulo C', 0.15, 'Tandil'),
('Articulo D', 1.45, 'Olavarria');

insert into envio
(id_proveedor, id_articulo, cantidad)
values
(1, 1, 10),
(1, 2, 25),
(1, 3, 8),
(2, 1, 5),
(2, 2, 13),
(2, 3, 4),
(2, 4, 20),
(3, 3, 12),
(3, 4, 9),
(1, 1, 8),
(1, 2, 10),
(1, 1, 7)

