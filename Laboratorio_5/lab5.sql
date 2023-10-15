CREATE TABLE superheroes.CBaleRico_Character (
    id serial primary key,
    name varchar (255) not null
);

CREATE TABLE superheroes.CBaleRico_Superheroe (
    id_character bigint not null,
    name varchar (255) not null,
    intelligence integer,
    strenght     integer,
    speed        integer,
    primary key (id_character),
    foreign key (id_character) references  superheroes.CBaleRico_Character(id)
);

CREATE TABLE superheroes.CBaleRico_Relation (
    id serial primary key,
    name varchar (255) not null,
);

CREATE TABLE superheroes.CBaleRico_Alterego (
    id serial primary key,
    name varchar (255) not null,
);

CREATE TABLE superheroes.CBaleRico_WorkOcupation (
    id serial primary key,
    name varchar (255) not null,
);

CREATE TABLE superheroes.CBaleRico_related_to (
    id_relation   bigint not null,
    id_character  bigint not null,
    id_superheroe bigint not null,

    primary key (id_relation, id_character, id_superheroe),
    foreign key id_character  references superheroes.CBaleRico_Character(id),
    foreign key id_superheroe references superheroes.CBaleRico_Superheroe(id_character),
    foreign key id_relation   references superheroes.CBaleRico_Relation(id)

);

CREATE TABLE superheroes.CBaleRico_hasWork (
    id_work       bigint not null,
    id_superheroe bigint not null,
    primary key (id_work, id_superheroe),
    foreign key id_workOcupation references superheroes.CBaleRico_WorkOcupation(id),
    foreign key id_superheroe    references superheroes.CBaleRico_Superheroe(id_Character),
);

CREATE TABLE superheroes.CBaleRico_hasAlterEgo (
    id_alter bigint not null,
    id_superheroe bigint not null,
    primary key (id_alter, id_superheroe),
    foreign key id_alter      references superheroes.CBaleRico_Alterego(id),
    foreign key id_superheroe references superheroes.CBaleRico_Superheroe(id_character),
);