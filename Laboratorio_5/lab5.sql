-- ############################# --
-- ###      INTEGRANTES      ### --   
-- ############################# --
-- ###      Martín Bravo     ### --
-- ###    Franco González    ### --
-- ###      Iván Vidal       ### --
-- ############################# --


-- ############################# --
-- ###          P1           ### --
-- ############################# --

-- Tabla de personajes
CREATE TABLE superheroes.CBaleRico_Character (
    id serial primary key,
    name varchar (255) not null
);

-- Tabla de superhéroes
CREATE TABLE superheroes.CBaleRico_Superheroe (
    id_character bigint not null,
    name varchar (255) not null,
    intelligence integer,
    strength     integer,
    speed        integer,
    primary key (id_character),
    foreign key (id_character) references  superheroes.CBaleRico_Character(id)
);

-- Tabla de relacion de personajes
CREATE TABLE superheroes.CBaleRico_Relation (
    id serial primary key,
    name varchar (255) not null
);

-- Tabla de alteregos
CREATE TABLE superheroes.CBaleRico_Alterego (
    id serial primary key,
    name varchar (255) not null
);

-- Tabla de ocupaciones
CREATE TABLE superheroes.CBaleRico_WorkOcupation (
    id serial primary key,
    name varchar (255) not null
);

-- Tabla de relacionado a
CREATE TABLE superheroes.CBaleRico_related_to (
    id_relation   bigint not null,
    id_character  bigint not null,
    id_superheroe bigint not null,

    primary key (id_relation, id_character, id_superheroe),
    foreign key (id_relation)   references superheroes.CBaleRico_Relation(id),
    foreign key (id_character)  references superheroes.CBaleRico_Character(id),
    foreign key (id_superheroe) references superheroes.CBaleRico_Superheroe(id_character)
);

-- Tabla de tiene trabajo
CREATE TABLE superheroes.CBaleRico_hasWork (
    id_workocupation bigint not null,
    id_superheroe    bigint not null,
    primary key (id_workocupation, id_superheroe),
    foreign key (id_workocupation) references superheroes.CBaleRico_WorkOcupation(id),
    foreign key (id_superheroe)    references superheroes.CBaleRico_Superheroe(id_Character)
);

-- Tabla de tiene alterego
CREATE TABLE superheroes.CBaleRico_hasAlterego (
    id_alterego   bigint not null,
    id_superheroe bigint not null,
    primary key (id_alterego, id_superheroe),
    foreign key (id_alterego)   references superheroes.CBaleRico_Alterego(id),
    foreign key (id_superheroe) references superheroes.CBaleRico_Superheroe(id_character)
);


-- ############################# --
-- ###          P3           ### --
-- ############################# --

-- (a)
-- Nombres de los 3 superheroes con más parientes.
SELECT S.name
FROM   superheroes.CBaleRico_Superheroe AS S,
       superheroes.CBaleRico_related_to AS R
WHERE  S.id_character = R.id_superheroe
GROUP BY (S.name, S.id_character)
ORDER BY count(DISTINCT R.id_character) DESC
LIMIT 3;

-- (b)
-- Nombres de los 3 personajes no superheroes con más parientes.
SELECT C.name, count(distinct R.id_superheroe)
FROM   superheroes.CBaleRico_Character  AS C,
       superheroes.CBaleRico_related_to AS R
WHERE  C.id = R.id_character
AND    C.id NOT IN (
    SELECT id_character
    FROM superheroes.CBaleRico_Superheroe
)
GROUP BY (C.name, C.id)
ORDER BY count(DISTINCT R.id_superheroe) DESC
LIMIT 3;

-- (c)
-- Nombres de los 5 superheroes con más parientes superheroes.
SELECT S.name
FROM   superheroes.CBaleRico_Superheroe AS S,
       superheroes.CBaleRico_related_to AS R
WHERE  S.id_character = R.id_superheroe
AND    R.id_character IN (
    SELECT id_character
    FROM superheroes.CBaleRico_Superheroe
)
GROUP BY (S.name, S.id_character)
ORDER BY count(DISTINCT R.id_character) DESC
LIMIT 5;

-- (d)
-- Nombre de relación más común.
SELECT relation.name
FROM   superheroes.CBaleRico_Relation   AS relation,
       superheroes.CBaleRico_related_to AS rel_to
WHERE  relation.id = rel_to.id_relation
GROUP BY (relation.id, relation.name)
ORDER BY count((rel_to.id_superheroe,rel_to.id_character)) DESC
LIMIT 1;

-- (e)
-- Los 3 trabajos más populares.
SELECT work.name
FROM   superheroes.CBaleRico_WorkOcupation AS work,
       superheroes.CBaleRico_hasWork       AS has
WHERE  work.id = has.id_workocupation
GROUP BY (work.id, work.name)
ORDER BY count(has.id_superheroe) DESC
LIMIT 3;


