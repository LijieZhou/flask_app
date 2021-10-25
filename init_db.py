import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO recipes (title, content) VALUES (?,?)",
           ('Thanksgiving IPA', 'hops, hops, a lot of hops')
           )
cur.execute("INSERT INTO recipes (title, content) VALUES (?,?)",
           ('Christmas coffee Stout', 'coffee, coffee, a lot of coffee')
           )
connection.commit()
connection.close()
