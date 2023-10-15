import psycopg2
import psycopg2.extras
import csv
import re

nombre_grupo = "superheroes.CBaleRico_"

def replace_inside_parentheses(match):
    return match.group(0).replace(" ", "-")

def del_inside_parentheses(s):
    return re.sub(r"\([^)]*\)","", s).strip()

cur = None
def findOrInsert(table, name):
    cur.execute("select id from "+ nombre_grupo+table +" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    cur.execute("insert into "+ nombre_grupo+table +" (name) values (%s) returning id", [name])
    return cur.fetchone()[0]

conn = psycopg2.connect (
    host     = "cc3201.dcc.uchile.cl",
    database = "cc3201",
    user     = "cc3201",
    password = "j'<3_cc3201",
    port     = "5440"
)
cur = conn.cursor()

with open("data.csv","r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
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
            name = row[index_name_char].strip()
        else:
            name = row[index_name_superh].strip()
        if "/" in name:
            name = name.split("/")[0].strip()
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
        cur.execute("insert into "+nombre_grupo+"Character (name) values (%s) returning id", [name])
        id_char = cur.fetchone()[0]

        ## Superheroe
        cur.execute("insert into "+nombre_grupo+"Superheroe (id_character, name, intelligence, strength, speed) values (%s, %s, %s, %s, %s)",
                    [id_char, name_super, intelligence, strength, speed])

        
        ## WorkOcupation
        if works:
            for work in works:
                # has 
                id_work = findOrInsert("WorkOcupation", work)

                cur.execute("select id_workocupation from "+nombre_grupo+"hasWork" +
                            " where id_workocupation=%s and id_superheroe=%s limit 1",
                            [id_work, id_char])
                r = cur.fetchone()
                if not r:
                    cur.execute("insert into "+nombre_grupo+"hasWork"+
                                "(id_workocupation, id_superheroe) values (%s, %s)",
                                [id_work, id_char])

        # Alterego
        if alter_egos:
            for alter_ego in alter_egos:
                id_alterego = findOrInsert("Alterego", alter_ego)
                cur.execute("insert into "+nombre_grupo+"hasAlterego"+
                            " (id_alterego, id_superheroe) values (%s, %s)",
                            [id_alterego, id_char])


# Leer de nuevo para las relaciones
with open("data.csv","r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            index_name_superh = row.index("name")
            index_name_char   = row.index("biography__full-name")
            index_relation    = row.index("connections__relatives")
            continue ##jump to next iteration

        # Full Name
        if row[index_name_char] and row[index_name_char] != "-":
            name = row[index_name_char].strip()
        else:
            name = row[index_name_superh].strip()
        if "/" in name:
            name = name.split("/")[0].strip()
        if "(" in name:
            name = del_inside_parentheses(name) # elimina el interior del parentesis

        relations = row[index_relation] if row[index_relation]!="-" else None
        if relations:
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

                                # id super
                                id_relation   = findOrInsert("Relation",   relation_type)
                                id_superheroe = findOrInsert("Character",  name)
                                id_character  = findOrInsert("Character",  name_related)

                                cur.execute("select id_relation from "+nombre_grupo+"related_to"+
                                            " where id_relation=%s and id_character=%s and id_superheroe=%s limit 1",
                                            [id_relation, id_character, id_superheroe])
                                r = cur.fetchone()
                                if not r:
                                    cur.execute("insert into "+nombre_grupo+"related_to"+
                                                " (id_relation, id_character, id_superheroe) values (%s, %s, %s)",
                                                [id_relation, id_character, id_superheroe])

conn.commit()
conn.close()
