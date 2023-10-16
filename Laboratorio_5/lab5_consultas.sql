
SELECT S.name, count(DISTINCT (R.id_relation, R.id_character)) AS count
FROM superheroes.CBaleRico_Superheroe AS S,
     superheroes.CBaleRico_related_to AS R

WHERE S.id_character = R.id_superheroe
GROUP BY (S.name, R.id_superheroe)

ORDER BY count DESC
LIMIT 3
;