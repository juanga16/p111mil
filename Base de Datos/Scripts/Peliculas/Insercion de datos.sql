-- inserto paises
insert into pais
(nombre)
values
('Argentina'),
('España'),
('Estados Unidos');

-- inserto generos
insert into genero
(nombre)
values
('Drama'),
('Misterio'),
('Romance'),
('Comedia'),
('Thriller');

-- inserto actores
insert into actor
(nombre, apellido, genero, fecha_nacimiento, id_pais)
values
('Ricardo', 'Darin', 'M', '1957-01-16', (select id from pais where nombre = 'Argentina')),
('Guillermo', 'Francella', 'M', '1955-02-14', (select id from pais where nombre = 'Argentina')),
('Soledad', 'Villamil', 'F', '1969-06-19', (select id from pais where nombre = 'Argentina')),
('Oscar', 'Martinez', 'M', '1949-10-23', (select id from pais where nombre = 'Argentina')),
('Norma', 'Aleandro', 'F', '1936-05-02', (select id from pais where nombre = 'Argentina'));

-- inserto directores
insert into director
(nombre, apellido, genero, fecha_nacimiento, id_pais)
values
('Juan Jose', 'Campanella', 'M', '1959-07-19', (select id from pais where nombre = 'Argentina')),
('Damian', 'Szifron', 'M', '1975-07-09', (select id from pais where nombre = 'Argentina'));

-- inserto peliculas
insert into pelicula
(titulo, anio, puntuacion, id_director)
values
('El secreto de sus ojos', 2009, 8.2, 1),
('Relatos salvajes', 2014, 8.1, 2),
('El hijo de la novia', 2001, 7.9, 1),
('El mismo amor, la misma lluvia', 1999, 7.4, 2);

-- inserto pelicula_genero
insert into pelicula_genero
(id_pelicula, id_genero)
values
((select id from pelicula where titulo = 'El secreto de sus ojos'), (select id from genero where nombre = 'Drama')),
((select id from pelicula where titulo = 'El secreto de sus ojos'), (select id from genero where nombre = 'Misterio')),
((select id from pelicula where titulo = 'El secreto de sus ojos'), (select id from genero where nombre = 'Romance')),
((select id from pelicula where titulo = 'Relatos salvajes'), (select id from genero where nombre = 'Comedia')),
((select id from pelicula where titulo = 'Relatos salvajes'), (select id from genero where nombre = 'Drama')),
((select id from pelicula where titulo = 'Relatos salvajes'), (select id from genero where nombre = 'Thriller')),
((select id from pelicula where titulo = 'El hijo de la novia'), (select id from genero where nombre = 'Comedia')),
((select id from pelicula where titulo = 'El hijo de la novia'), (select id from genero where nombre = 'Drama')),
((select id from pelicula where titulo = 'El mismo amor, la misma lluvia'), (select id from genero where nombre = 'Comedia')),
((select id from pelicula where titulo = 'El mismo amor, la misma lluvia'), (select id from genero where nombre = 'Drama')),
((select id from pelicula where titulo = 'El mismo amor, la misma lluvia'), (select id from genero where nombre = 'Romance'));

-- inserto pelicula_pais
insert into pelicula_pais
(id_pelicula, id_pais)
values
((select id from pelicula where titulo = 'El secreto de sus ojos'), (select id from pais where nombre = 'Argentina')),
((select id from pelicula where titulo = 'El secreto de sus ojos'), (select id from pais where nombre = 'España')),
((select id from pelicula where titulo = 'Relatos salvajes'), (select id from pais where nombre = 'Argentina')),
((select id from pelicula where titulo = 'Relatos salvajes'), (select id from pais where nombre = 'España')),
((select id from pelicula where titulo = 'El hijo de la novia'), (select id from pais where nombre = 'Argentina')),
((select id from pelicula where titulo = 'El hijo de la novia'), (select id from pais where nombre = 'España')),
((select id from pelicula where titulo = 'El mismo amor, la misma lluvia'), (select id from pais where nombre = 'Argentina')),
((select id from pelicula where titulo = 'El mismo amor, la misma lluvia'), (select id from pais where nombre = 'Estados Unidos'));

-- inserto actorPeliculas
insert into pelicula_actor
(id_pelicula, id_actor)
values
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 1),
(3, 1),
(4, 1),
(4, 3);
