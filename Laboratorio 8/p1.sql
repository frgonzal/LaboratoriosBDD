-- a

SELECT COUNT (*)
FROM opt.pelicula10000;
-- 6401

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'pelicula10000';
-- 52

-- Tuplas por bloque: 6401/52 = 123.1


SELECT COUNT (*)
FROM opt.actor10000;
-- 197219

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'actor10000';
-- 1215

-- Tuplas por bloque: 197219/1215 = 162.3

SELECT COUNT (*)
FROM opt.personaje10000;
-- 372367

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'personaje10000';
-- 3684

-- Tuplas por bloque: 372367/3684 = 101.0

SELECT COUNT (*)
FROM opt.pelicula1000;
-- 22490

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'pelicula1000';
-- 183

-- Tuplas por bloque: 22490/183 = 122.9

FROM opt.actor1000;
SELECT COUNT (*)
-- 440234

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'actor1000';
-- 2712

-- Tuplas por bloque: 440234/2712 = 162.3

SELECT COUNT (*)
FROM opt.personaje1000;
-- 944964

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'personaje1000';
-- 9330

-- Tuplas por bloque: 944964/9330 = 101.3

SELECT COUNT (*)
FROM opt.pelicula100;
--72696

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'pelicula100';
-- 598

-- Tuplas por bloque: 72696/598 = 121.5

SELECT COUNT (*)
FROM opt.actor100;
-- 856421

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'actor100';
-- 5278

-- Tuplas por bloque: 856421/5278 = 162.3

SELECT COUNT (*)
FROM opt.personaje100;
-- 2170526

SELECT DISTINCT relname, relpages
FROM pg_class
WHERE relname = 'personaje100';
-- 21410

-- Tuplas por bloque: 2170526/21410 = 101.4

-- b

EXPLAIN ANALYZE 
SELECT * 
FROM opt.personaje100 
WHERE p_nombre='Up' 
AND p_anho=2009;
'''
                                                         QUERY PLAN                                                          
-----------------------------------------------------------------------------------------------------------------------------
 Gather  (cost=1000.00..35975.99 rows=2 width=47) (actual time=8.028..164.199 rows=33 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on personaje100  (cost=0.00..34975.79 rows=1 width=47) (actual time=4.146..144.799 rows=11 loops=3)
         Filter: (((p_nombre)::text = 'Up'::text) AND (p_anho = 2009))
         Rows Removed by Filter: 723498
 Planning Time: 0.209 ms
 Execution Time: 164.261 ms
(8 rows)

'''

EXPLAIN ANALYZE 
SELECT * 
FROM opti.personaje100 
WHERE p_nombre='Up' 
AND p_anho=2009;

'''
                                                                QUERY PLAN                                                                
------------------------------------------------------------------------------------------------------------------------------------------
 Index Scan using personaje100_pnombreanho on personaje100  (cost=0.43..12.47 rows=2 width=47) (actual time=0.046..0.118 rows=33 loops=1)
   Index Cond: (((p_nombre)::text = 'Up'::text) AND (p_anho = 2009))
 Planning Time: 0.651 ms
 Execution Time: 0.168 ms
(4 rows)
'''

-- c

-- opt lee 21410 bloques


-- mejor caso 1 peor 33
-- opti lee 33 bloques, ya que está indexado y nos permite acceder directamente a los bloques que contienen las tuplas que cumplen la condición

-- P2

