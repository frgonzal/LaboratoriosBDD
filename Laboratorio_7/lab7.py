import psycopg2
import matplotlib.pyplot as plt


conn = psycopg2.connect (
    host     = "cc3201.dcc.uchile.cl",
    database = "cc3201",
    user     = "cc3201",
    password = "j'<3_cc3201",
    port     = "5440"
)
cur = conn.cursor()

def time_cons(tamanno: int, optimizacion: str, anidada: bool):

    if anidada:
        consulta = f"""
            explain analyze
            select distinct pelicula.nombre, pelicula.anho
            from  {optimizacion}.pelicula{tamanno} as pelicula, {optimizacion}.personaje{tamanno} as personaje
            where pelicula.nombre = personaje.p_nombre
            and   pelicula.anho   = personaje.p_anho
            and   personaje.a_nombre in (
                select  personaje.a_nombre 
                from    {optimizacion}.pelicula{tamanno} as pelicula, {optimizacion}.personaje{tamanno} as personaje
                where   personaje.p_nombre = pelicula.nombre
                and     pelicula.nombre = 'Inception'
            );"""
    else:
        consulta = f"""
            explain analyze
            select distinct pelicula1.nombre, pelicula1.anho
            from    {optimizacion}.pelicula{tamanno} as pelicula1,
                    {optimizacion}.personaje{tamanno} as personaje1,
                    {optimizacion}.pelicula{tamanno} as pelicula2,
                    {optimizacion}.personaje{tamanno} as personaje2
            where pelicula1.nombre = personaje1.p_nombre
            and   pelicula1.anho   = personaje1.p_anho
            and   pelicula2.nombre = personaje2.p_nombre
            and   pelicula2.anho   = personaje2.p_anho
            and   pelicula2.nombre = 'Inception'
            and   personaje2.a_nombre = personaje1.a_nombre;
            """

    cur.execute(consulta)
    r = cur.fetchone()

    while (r):
        r = r[0]
        if("Planning Time" in r):
            p_time = r
        if("Execution Time" in r):
            e_time = r
        r = cur.fetchone()
    return  p_time, e_time



ns = [100, 1000, 10000]

print("consulta anidada optimizada")
for n in ns:
    print(str(n)+":"+" "*(6 - len(str(n))),time_cons(n, "opti", True))

print("consulta no anidada optimizada")
for n in ns:
    print(str(n)+":"+" "*(6 - len(str(n))),time_cons(n, "opti", False))

print("consulta anidada no optimizada")
for n in ns:
    print(str(n)+":"+" "*(6 - len(str(n))),time_cons(n, "opt", True))

print("consulta no anidada no optimizada")
y = []
z = []
for n in ns:
    y.append(time_cons(n, "opt", False)[0])
    z.append(time_cons(n, "opt", False)[1])
    print(str(n)+":"+" "*(6 - len(str(n))),time_cons(n, "opt", False))

plt.plot(ns, y, label='Line', color='r', linestyle='-')
plt.plot(ns, z, label='Line', color='b', linestyle='-')

plt.show()

conn.close()







