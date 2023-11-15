-- P1

DROP TABLE IF EXISTS trx_p.Abdiuk_votosPorCondado;
DROP TABLE IF EXISTS trx_p.Abdiuk_candidato;
DROP TABLE IF EXISTS trx_p.Abdiuk_condado;
DROP TABLE IF EXISTS trx_p.Abdiuk_estado;

CREATE TABLE trx_p.Abdiuk_estado (
    nombre varchar (255),
	voto_electoral smallint,
	cierre time,
	num_candidatos smallint,
	primary key (nombre)
);

INSERT INTO Abdiuk_estado SELECT * FROM estado;

CREATE TABLE trx_p.Abdiuk_condado (
    nombre varchar (255),
	estado varchar (255),
	reportado float,
    check (reportado >= 0 and reportado <= 1),
	primary key (nombre, estado),
	foreign key (estado) references Abdiuk_estado(nombre)
);

INSERT INTO Abdiuk_condado SELECT * FROM condado;

CREATE TABLE trx_p.Abdiuk_candidato (
    nombre varchar (255),
	partido varchar (255),
	primary key (nombre)
);

INSERT INTO Abdiuk_candidato SELECT * FROM candidato;

CREATE TABLE trx_p.Abdiuk_votosPorCondado (
    candidato varchar (255),
	condado varchar (255),
	estado varchar (255),
    votos int,
	primary key (candidato, condado, estado),
	foreign key (candidato) references Abdiuk_candidato(nombre),
	foreign key (condado, estado) references Abdiuk_condado(nombre, estado)
);

INSERT INTO Abdiuk_votosPorCondado SELECT * FROM votosPorCondado;

-- P2

UPDATE trx_p.Abdiuk_votosPorCondado
SET votos = A1.votos + Abdiuk_votosPorCondado.votos
FROM votosPorCondado1 AS A1
WHERE Abdiuk_votosPorCondado.candidato = A1.candidato
AND Abdiuk_votosPorCondado.condado = A1.condado 
AND Abdiuk_votosPorCondado.estado = A1.estado;

-- P3

UPDATE trx_p.Abdiuk_condado
SET reportado = C1.reportado
FROM condado1 AS C1
WHERE Abdiuk_condado.nombre = C1.nombre
AND Abdiuk_condado.estado = C1.estado;

-- P4

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A2.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado2 AS A2
    WHERE Abdiuk_votosPorCondado.candidato = A2.candidato
    AND Abdiuk_votosPorCondado.condado = A2.condado
    AND Abdiuk_votosPorCondado.estado = A2.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C2.reportado
    FROM condado2 AS C2
    WHERE Abdiuk_condado.nombre = C2.nombre
    AND Abdiuk_condado.estado = C2.estado;
COMMIT;

-- P5

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A3.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado3 AS A3
    WHERE Abdiuk_votosPorCondado.candidato = A3.candidato
    AND Abdiuk_votosPorCondado.condado = A3.condado
    AND Abdiuk_votosPorCondado.estado = A3.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C3.reportado
    FROM condado3 AS C3
    WHERE Abdiuk_condado.nombre = C3.nombre
    AND Abdiuk_condado.estado = C3.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A4.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado4 AS A4
    WHERE Abdiuk_votosPorCondado.candidato = A4.candidato
    AND Abdiuk_votosPorCondado.condado = A4.condado
    AND Abdiuk_votosPorCondado.estado = A4.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C4.reportado
    FROM condado4 AS C4
    WHERE Abdiuk_condado.nombre = C4.nombre
    AND Abdiuk_condado.estado = C4.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A5.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado5 AS A5
    WHERE Abdiuk_votosPorCondado.candidato = A5.candidato
    AND Abdiuk_votosPorCondado.condado = A5.condado
    AND Abdiuk_votosPorCondado.estado = A5.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C5.reportado
    FROM condado5 AS C5
    WHERE Abdiuk_condado.nombre = C5.nombre
    AND Abdiuk_condado.estado = C5.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A6.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado6 AS A6
    WHERE Abdiuk_votosPorCondado.candidato = A6.candidato
    AND Abdiuk_votosPorCondado.condado = A6.condado
    AND Abdiuk_votosPorCondado.estado = A6.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C6.reportado
    FROM condado6 AS C6
    WHERE Abdiuk_condado.nombre = C6.nombre
    AND Abdiuk_condado.estado = C6.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A7.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado7 AS A7
    WHERE Abdiuk_votosPorCondado.candidato = A7.candidato
    AND Abdiuk_votosPorCondado.condado = A7.condado
    AND Abdiuk_votosPorCondado.estado = A7.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C7.reportado
    FROM condado7 AS C7
    WHERE Abdiuk_condado.nombre = C7.nombre
    AND Abdiuk_condado.estado = C7.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A8.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado8 AS A8
    WHERE Abdiuk_votosPorCondado.candidato = A8.candidato
    AND Abdiuk_votosPorCondado.condado = A8.condado
    AND Abdiuk_votosPorCondado.estado = A8.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C8.reportado
    FROM condado8 AS C8
    WHERE Abdiuk_condado.nombre = C8.nombre
    AND Abdiuk_condado.estado = C8.estado;
COMMIT;

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = A9.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondado9 AS A9
    WHERE Abdiuk_votosPorCondado.candidato = A9.candidato
    AND Abdiuk_votosPorCondado.condado = A9.condado
    AND Abdiuk_votosPorCondado.estado = A9.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = C9.reportado
    FROM condado9 AS C9
    WHERE Abdiuk_condado.nombre = C9.nombre
    AND Abdiuk_condado.estado = C9.estado;
COMMIT;

-- P6

START TRANSACTION;
    UPDATE trx_p.Abdiuk_votosPorCondado
    SET votos = AX.votos + Abdiuk_votosPorCondado.votos
    FROM votosPorCondadoX AS AX
    WHERE Abdiuk_votosPorCondado.candidato = AX.candidato
    AND Abdiuk_votosPorCondado.condado = AX.condado
    AND Abdiuk_votosPorCondado.estado = AX.estado;
    UPDATE trx_p.Abdiuk_condado
    SET reportado = CX.reportado
    FROM condadoX AS CX
    WHERE Abdiuk_condado.nombre = CX.nombre
    AND Abdiuk_condado.estado = CX.estado;
COMMIT;

SELECT * FROM votosPorCondadoX;
SELECT * FROM condadoX;

-- ERROR:  new row for relation "abdiuk_condado" violates check constraint "abdiuk_condado_reportado_check"
-- DETAIL:  Failing row contains (Real County, Texas, 100).
-- ROLLBACK
-- Putin no lo logró, trataron de poner reportado de Texas en 100 pero debe ser un valor entre 0 y 1
