import psycopg2

def drop_table(cur):
    cur.execute("""DROP TABLE phones;
                   DROP TABLE people;""")


def create_db(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS people(
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(40) NOT NULL,
                    email VARCHAR(40) UNIQUE NOT NULL);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
                    id SERIAL PRIMARY KEY,
                    people_id INTEGER NOT NULL REFERENCES people(id),
                    phone VARCHAR UNIQUE NOT NULL);""")


def new_client(cur, name, surname, email, phone=None):
    if phone == None:
        cur.execute("""INSERT INTO people(name,surname,email)
                       VALUES(%s, %s, %s);""", (name,surname,email))
        cur.execute("""SELECT *FROM people;""")
        print(cur.fetchall(), end="\n\n")
    else:
        cur.execute("""INSERT INTO people(name,surname,email)
                       VALUES(%s, %s, %s);""", (name,surname,email))
        cur.execute("""SELECT *FROM people;""")
        print(cur.fetchall())
        cur.execute("""INSERT INTO phones(people_id,phone)
                       VALUES((SELECT id FROM people where email=%s),%s);""", (email, phone))
        cur.execute("""SELECT *FROM phones;""")
        print(cur.fetchall(), end="\n\n")



def add_phone(cur, people_id, phone):
    cur.execute("""INSERT INTO phones(people_id,phone)
                   VALUES(%s,%s);""", (people_id, phone))
    cur.execute("""SELECT *FROM phones;""")
    print(cur.fetchall(), end="\n\n")


def count_phones(cur,people_id):
    cur.execute("""SELECT COUNT(*) FROM phones WHERE people_id = %s;""", (people_id,))
    amount = cur.fetchall()[0][0]
    return amount


def change_client(cur, people_id, name=None, surname=None, email=None, phone=None):
    if name != None:
        cur.execute("""UPDATE people
                          SET name = %s
                        WHERE id = %s;""", (name,people_id))
    if surname != None:
        cur.execute("""UPDATE people
                          SET surname = %s
                        WHERE id = %s;""", (surname,people_id))
    if email != None:
        cur.execute("""UPDATE people
                          SET email = %s
                        WHERE id = %s;""", (email,people_id))
    if phone != None and count_phones(cur,people_id) == 1:
        cur.execute("""UPDATE phones
                          SET phone = %s
                        WHERE people_id = %s;""", (phone,people_id))
        cur.execute("""SELECT *FROM phones;""")
        print(cur.fetchall())
    elif phone != None and count_phones(cur,people_id) > 1:
        number = input("Какой номер вы хотите изменить?")
        cur.execute("""UPDATE phones
                          SET phone = %s
                        WHERE phone = %s;""", (phone,number))
        cur.execute("""SELECT *FROM phones;""")
        print(cur.fetchall())
    cur.execute("""SELECT *FROM people;""")
    print(cur.fetchall(), end="\n\n")


def delete_phone(cur, people_id, phone):
    cur.execute("""DELETE FROM phones WHERE phone = %s and people_id = %s;""", (phone,people_id))
    cur.execute("""SELECT *FROM phones;""")
    print(cur.fetchall(), end="\n\n")


def delete_client(cur, people_id):
    cur.execute("""DELETE FROM phones WHERE people_id = %s;""", (people_id,))
    cur.execute("""SELECT *FROM phones;""")
    print(cur.fetchall())
    cur.execute("""DELETE FROM people WHERE id = %s;""", (people_id,))
    cur.execute("""SELECT *FROM people;""")
    print(cur.fetchall(), end="\n\n")


def find_client(cur, **info):
    stri ="SELECT name, surname , email , phone \
             FROM people p \
                  LEFT JOIN phones p2 ON p.id = p2.people_id \
            WHERE " + ' and '.join(f"{c} like '{v}'" for c, v in info.items()) + ";"
    cur.execute(stri)
    print(cur.fetchall(), end="\n\n")



if __name__ == '__main__':
    with psycopg2.connect(database='HW', user='postgres', password='...') as con:
        with con.cursor() as cur:
            drop_table(cur)
            create_db(cur)
            new_client(cur,'Mariya','Orlova','mariya45@mail.ru', '79135643098')
            new_client(cur,'Alina','Gubareva','gubar@mail.ru')
            new_client(cur,'Nikita','Levchuk','nikLev@mail.ru', '79149004567')
            add_phone(cur,3,'79156978422')
            change_client(cur,2,'Aleftina', surname='Levchuk')
            change_client(cur,3,phone='792098764391')
            delete_phone(cur, 3, '792098764391')
            delete_client(cur,3)
            find_client(cur,surname='Levchuk')
            con.commit()
    con.close()