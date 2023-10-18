SELECT *
FROM uchile.transparencia
WHERE apellido_p='Saure'
ORDER BY total DESC;


SELECT nombre, nota
FROM nota.cc3201
WHERE nombre='González Leiva, Franco Antonio'
   or nombre='Vidal Romero, Iván Mauricio';

UPDATE nota.cc3201
SET nota = 7
WHERE nombre='González Leiva, Franco Antonio'
   or nombre='Vidal Romero, Iván Mauricio';


SELECT table_name, table_schema FROM information_schema.tables;

SELECT column_name, data_type FROM information_schema.columns
WHERE table_name='cc3201' AND table_schema='nota';



';SELECT table_name, table_schema FROM information_schema.tables;--'

';SELECT column_name, data_type FROM information_schema.columns
WHERE table_name='cc3201' AND table_schema='nota';--'

';SELECT nombre, avg(nota) FROM nota.cc3201
 WHERE nombre='González Leiva, Franco Antonio'   
   or nombre='Vidal Romero, Iván Mauricio' GROUP BY nombre;--'

';UPDATE nota.cc3201
SET nota = 7
WHERE nombre='González Leiva, Franco Antonio'
   or nombre='Vidal Romero, Iván Mauricio';--'

';UPDATE nota.cc3201
SET comentario = 'Christian Bale Rico'
WHERE nombre='González Leiva, Franco Antonio'
   or nombre='Vidal Romero, Iván Mauricio';--'


';SELECT nombre, comentario
FROM nota.cc3201
WHERE nombre='González Leiva, Franco Antonio'
   or nombre='Vidal Romero, Iván Mauricio';--'



cur.execute("SELECT nombres, apellido_p, apellido_m, mes, anho, total FROM uchile.transparencia WHERE apellido_p='"+input+"' ORDER BY total DESC LIMIT 250")