import psycopg2
import psycopg2.extras
import csv
import re

def get_conn():
    conn = psycopg2.connect ( host =" cc3201 .dcc . uchile .cl",
        database =" cc3201 ",
        user =" cc3201 ",
        password ="j '< 3_cc3201 ", port =" 5440 ")
    return conn


def findOrInsert(table, name, cur):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]

with open("data.csv","r") as csvfile:
    names_super = []
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
            index_bueno              = row.index("biography__alignment")
            continue
        
        # Nombre completo de personaje
        if row[index_name_char] and row[index_name_char] != "-":
            name = row[index_name_char].strip()
        else:
            name = row[index_name_superh].strip()
        #char_id = findOrInsert("CBaleRico_Superheroe", name, )

        # Nombre superheroe
        name_super   = row[index_name_superh] 

        names_super.append(name)
        names_super.append(name_super)

        # Atributos
        intelligence = row[index_intelligence] if row[index_intelligence]!="null" else None
        strength     = row[index_strength] if row[index_strength]!="null" else None
        speed        = row[index_speed] if row[index_speed]!="null" else None

        #trabajo
        works = row[index_name_workOcupation] if row[index_name_workOcupation]!="-" else None
        if works:
            works = re.split(r"[,;]", works)
            works = [x.replace('"',"").replace("'","").strip() for x in works]
            works = [str(re.sub(r"\([^)]*\)","",x)).strip().lower() for x in works]


        # alter ego
        alter_egos = row[index_name_alter] if row[index_name_alter]!="No alter egos found." else None
        if alter_egos:
            alter_egos = re.split(r"[,;]", alter_egos)
            alter_egos = [x.strip() for x in alter_egos]

# Leer de nuevo para las relaciones
with open("data.csv","r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            index_relation = row.index("connections__relatives")
            continue ##jump to next iteration

        relations = row[index_relation] if row[index_relation]!="-" else None
        if relations:
            relationsc = relations
            def replace_inside_parentheses(match):
                return match.group(0).replace(" ", "-")

            relations = (relations.replace(";",",").replace(", ",",").replace('\n',"")
                                  .replace(" )",")").replace("( ","(") .replace("'","")
                                  .replace('"',"") .replace(") ,","),").replace('\\n',"")
                                  .replace(" ,",",")
                                  )
            relations = re.sub(r'\([^)]*\)', replace_inside_parentheses, relations)
            relations = relations.split("),")

            for relation in relations:
                if relation and (relation.count("(")!=relation.count(")")):
                    relation += ")"
                relation = relation.strip()

                m = relation
                relation = re.search("([^(]+)[ ]*\(([^) ]+)\)", relation)

                if relation:
                    name_related = relation.group(1).split(",")
                    name_related = list(filter(lambda x:
                                                x and\
                                                x != "Jr." and\
                                                "deceased" not in x.lower() and \
                                                "unnamed" not in x.lower() and\
                                                "unidentified" not in x.lower() and\
                                                x[0].isupper() #nombres comienzan con mayus
                                        , name_related))
                    name_related = [x.strip() for x in name_related]

                    relation_type = relation.group(2).split(",")
                    relation_type = list(filter(lambda x:
                                                    x and\
                                                    "deceased" not in x.lower() and \
                                                    "relatives" not in x.lower() and\
                                                    x.lower()!="unconfirmed" and\
                                                    x[0].islower() #relaciones comienzan con minus
                                            , relation_type))
                    if name_related and relation_type:
                        for k in range(len(relation_type)):
                            rel = relation_type[k]
                            if relation_type[k][-1] == "s":
                                rel = relation_type[k][:-1]
                            for nam in name_related:
                                print(str(i)+" "*(4-len(str(i)))+"name: ",nam," "*(40-len(str(nam))),"relation: ", rel)

