



explain analyze
select distinct pelicula.nombre, pelicula.anho
from  opti.pelicula10000 as pelicula, opti.personaje10000 as personaje
where pelicula.nombre = personaje.p_nombre
and   pelicula.anho   = personaje.p_anho
and   personaje.a_nombre in (
    select  personaje.a_nombre 
    from    opti.pelicula10000 as pelicula, opti.personaje10000 as personaje
    where   personaje.p_nombre = pelicula.nombre
    and     pelicula.nombre = 'Inception'
)
;

explain analyze
select distinct pelicula1.nombre, pelicula1.anho

from    opti.pelicula10000 as pelicula1,
        opti.personaje10000 as personaje1,
        opti.pelicula10000 as pelicula2,
        opti.personaje10000 as personaje2

-- peliculas en las que participaron actor1
where pelicula1.nombre = personaje1.p_nombre
and   pelicula1.anho   = personaje1.p_anho


-- actores que participaron en Inception
and   pelicula2.nombre = personaje2.p_nombre
and   pelicula2.anho   = personaje2.p_anho
and   pelicula2.nombre = 'Inception'

-- actor 1 == actor 2
and   personaje2.a_nombre = personaje1.a_nombre
;