#############################
###      INTEGRANTES      ###   
#############################
###      Martín Bravo     ###
###    Franco González    ###
###      Iván Vidal       ###
#############################
import psycopg2
import psycopg2.extras
import csv
import re

# Nombre del grupo para las tablas
nombre_grupo      = "superheroes.CBaleRico_"
 
# Tablas de entidades
T_character   = nombre_grupo + "Character"
T_superheroe  = nombre_grupo + "Superheroe"
T_relation    = nombre_grupo + "Relation"
T_work        = nombre_grupo + "WorkOcupation"
T_alterego    = nombre_grupo + "Alterego"

# Tablas de relaciones
T_related_to  = nombre_grupo + "related_to"
T_haswork     = nombre_grupo + "hasWork"
T_hasalterego = nombre_grupo + "hasAlterego"

# Funcion para reemplazar espacios por guiones
def replace_inside_parentheses(match):
    return match.group(0).replace(" ", "-")

# Funcion para eliminar el interior de los parentesis
def del_inside_parentheses(s):
    return re.sub(r"\([^)]*\)","", s).strip()

# Conexion a la base de datos
conn = psycopg2.connect (
    host     = "cc3201.dcc.uchile.cl",
    database = "cc3201",
    user     = "cc3201",
    password = "j'<3_cc3201",
    port     = "5440"
)
# Cursor
cur = conn.cursor()

# Funcion para buscar o insertar en una tabla
def findOrInsert(table, name):
    cur.execute("select id from "+ table +" where name=%s limit 1", [name]) # Buscar
    r = cur.fetchone()
    if(r): # Si existe
        return r[0]
    cur.execute("insert into "+ table +" (name) values (%s) returning id", [name])
    return cur.fetchone()[0] 

# Funcion para buscar o insertar en la tabla de characters
def insertChar(name):
    cur.execute("insert into "+T_character+" (name) values (%s) returning id", [name])
    return cur.fetchone()[0]

# Funcion para buscar o insertar en la tabla de characters
def findOrInsertCharacter(name_related):
    #Buscar en characters
    cur.execute("select id from "+T_character +" where name=%s limit 1", [name_related])
    id_character = cur.fetchone()
    # Buscar en superheroes
    if not id_character:
        cur.execute("select id_character from "+T_superheroe+" where name=%s limit 1", [name_related])
        id_character = cur.fetchone()
    # Insertar en characters
    if not id_character:
        cur.execute("insert into "+T_character+" (name) values (%s) returning id", [name_related])
        id_character = cur.fetchone()
    return id_character[0]

# Funcion para insertar en la tabla de superheroes
def insertSuperheroe(id_char, name_super, intelligence, strength, speed):
    cur.execute("select id_character from "+T_superheroe+" where id_character=%s and name=%s", [id_char, name_super])
    id_super = cur.fetchone()
    if not id_super:
        cur.execute("insert into "+ T_superheroe
                    +" (id_character, name, intelligence, strength, speed)"
                    +" values (%s, %s, %s, %s, %s)",
                    [id_char, name_super, intelligence, strength, speed])

# Funcion para insertar en la tabla de relaciones
def insertHasWork(id_work, id_char):
    cur.execute("select id_workocupation from "+ T_haswork
                +" where id_workocupation=%s and id_superheroe=%s limit 1",
                [id_work, id_char])
    r = cur.fetchone()
    if not r:
        cur.execute("insert into "+ T_haswork
                    +" (id_workocupation, id_superheroe) values (%s, %s)",
                    [id_work, id_char])

# Funcion para insertar en la tabla de relaciones
def insertHasAlter(id_alterego, id_char): 
    cur.execute("select id_alterego from "+ T_hasalterego
                +" where id_alterego=%s and id_superheroe=%s limit 1",
                [id_alterego, id_char])
    r = cur.fetchone()
    # Si no existe
    if not r:
        cur.execute("insert into "+ T_hasalterego
                    +" (id_alterego, id_superheroe) values (%s, %s)",
                    [id_alterego, id_char])

# Funcion para insertar en la tabla de relaciones
def insertHasRelation(id_relation, id_character, id_superheroe):
    cur.execute("select id_relation from " + T_related_to
                +" where id_relation=%s and id_character=%s and id_superheroe=%s limit 1",
                [id_relation, id_character, id_superheroe])
    r = cur.fetchone()
    # Si no existe
    if not r:
        cur.execute("insert into " + T_related_to
                    +" (id_relation, id_character, id_superheroe) values (%s, %s, %s)",
                    [id_relation, id_character, id_superheroe])

# Leer el archivo csv
with open("data.csv","r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            # Indices
            index_name_char          = row.index("biography__full-name")
            index_name_superh        = row.index("name")
            index_intelligence       = row.index("powerstats__intelligence") 
            index_strength           = row.index("powerstats__strength")
            index_speed              = row.index("powerstats__speed")
            index_name_workOcupation = row.index("work__occupation")
            index_name_alter         = row.index("biography__alter-egos")
            index_bueno              = row.index("biography__alignment") ## podria ser util ?
            continue
        
        # Nombre completo de personaje
        if row[index_name_char] and row[index_name_char] != "-":
            name = row[index_name_char]
        else:
            name = row[index_name_superh]
        if "/" in name:
            name = name.split("/")[0].strip() # separa por / y toma el primero
        if "(" in name:
            name = del_inside_parentheses(name) # elimina el interior del parentesis

        # Nombre superheroe
        name_super   = row[index_name_superh]

        # Atributos
        intelligence = row[index_intelligence] if row[index_intelligence]!="null" else None
        strength     = row[index_strength] if row[index_strength]!="null" else None
        speed        = row[index_speed] if row[index_speed]!="null" else None

        #trabajo
        works = row[index_name_workOcupation] if row[index_name_workOcupation]!="-" else None
        if works:
            works = re.split(r"[,;/]", works)
            works = [x.replace('"',"").replace("'","").strip() for x in works]
            works = [del_inside_parentheses(x).lower() for x in works]
            works = list(filter(lambda x: x, works))


        # alter ego
        alter_egos = row[index_name_alter] if row[index_name_alter]!="No alter egos found." else None
        if alter_egos:
            alter_egos = re.split(r"[,;]", alter_egos)
            alter_egos = [x.strip() for x in alter_egos]

        ###################################
        ###         Agregar             ###
        ###################################

        ## Character
        id_char = insertChar(name)

        ## Superheroe
        insertSuperheroe(id_char, name_super, intelligence, strength, speed)

        ## WorkOcupation
        if works:
            for work in works:
                id_work = findOrInsert(T_work, work)
                #has
                insertHasWork(id_work, id_char) 

        # Alterego
        if alter_egos:
            for alter_ego in alter_egos:
                id_alterego = findOrInsert(T_alterego, alter_ego)
                #has
                insertHasAlter(id_alterego, id_char)


# Leer de nuevo para las relaciones
with open("data.csv","r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            # Indices
            index_name_superh = row.index("name")
            index_name_char   = row.index("biography__full-name")
            index_relation    = row.index("connections__relatives")
            continue

        # Full Name
        if row[index_name_char] and row[index_name_char] != "-":
            name = row[index_name_char] # nombre completo
        else:
            name = row[index_name_superh] # nombre superheroe
        if "/" in name:
            name = name.split("/")[0].strip() # separa por / y toma el primero
        if "(" in name:
            name = del_inside_parentheses(name) # elimina el interior del parentesis

        # Relations
        relations = row[index_relation] if row[index_relation]!="-" else None
        if not relations: continue

        relations = (relations
                        .replace(";",",") .replace(", ",",")  .replace('\n',"")
                        .replace(" )",")").replace("( ","(")  .replace("'","")
                        .replace('"',"")  .replace(") ,","),").replace('\\n',"")
                        .replace(" ,",",")
                    )
        relations = re.sub(r'\([^)]*\)', replace_inside_parentheses, relations)
        relations = relations.split("),")
        for relation in relations:
            if relation and (relation.count("(")!=relation.count(")")):
                relation += ")"
            relation = relation.strip()
            relation = re.search("([^(]+)[ ]*\(([^) ]+)\)", relation)

            if relation:
                names_related = relation.group(1)
                names_related = re.split(r"[,/]", names_related)
                names_related = [x.strip() for x in names_related]
                names_related = list(filter(lambda x:
                                            x and\
                                            x != "Jr." and x != "Sr." and\
                                            "deceased" not in x.lower() and \
                                            "unnamed" not in x.lower() and\
                                            "unidentified" not in x.lower() and\
                                            x[0].isupper() #nombres comienzan con mayus
                                    , names_related))

                relations_type = relation.group(2)
                relations_type = re.split(r"[,/]", relations_type)
                relations_type = [x.replace("(","").replace(")","").strip() for x in relations_type]
                relations_type = list(filter(lambda x:
                                                x and\
                                                x.lower()!="deceased" and \
                                                x.lower()!="status-unknown" and\
                                                "relatives" not in x.lower() and\
                                                x.lower()!="unconfirmed" and\
                                                x[0].islower() #relaciones comienzan con minus
                                        , relations_type))

                if names_related and relations_type:
                    for relation_type in relations_type:
                        if relations_type[-1] == "s": # si esta en plural
                            relation_type = relations_type[:-1]
                        for name_related in names_related:
                            ##########################
                            ##      Relaciones      ##
                            ##########################

                            # id relation
                            id_relation   = findOrInsert(T_relation, relation_type)
                            # id superheroe
                            id_superheroe = findOrInsert(T_character, name)
                            # id character
                            id_character = findOrInsertCharacter(name_related)

                            # insert relation
                            insertHasRelation(id_relation, id_character, id_superheroe)

conn.commit()
conn.close()
