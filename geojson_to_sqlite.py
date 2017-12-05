import json
import sqlite3



json_filename = 'data/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
db_filename = 'data/arbres.db'

data = json.load(open( json_filename ))

db = sqlite3.connect(db_filename)

# -- create the table --
cursor = db.cursor()

cursor.execute("""  DROP TABLE IF EXISTS arbres  """)
db.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS arbres (
                     id INTEGER PRIMARY KEY,
                     code_parent_desc TEXT,
                     code_parent TEXT,
                     genre_bota TEXT,
                     espece TEXT,
                     variete TEXT,
                     anneedeplantation INTEGER,
                     stadededeveloppement TEXT,
                     sous_categorie_desc TEXT,
                     sous_categorie TEXT,
                     longitude REAL,
                     latitude REAL
                )
                """)


db.commit()

# -- Populate the table --
arbres = []

for k, arbre in enumerate( data['features'] ):
    infolist = []
    infolist.append( arbre['properties']['CODE_PARENT_DESC'] )
    infolist.append( arbre['properties']['CODE_PARENT'] )
    infolist.append( arbre['properties']['GENRE_BOTA'] )
    infolist.append( arbre['properties']['ESPECE'] )
    infolist.append( arbre['properties']['VARIETE'] )
    infolist.append( arbre['properties']['ANNEEDEPLANTATION'] )
    infolist.append( arbre['properties']['STADEDEDEVELOPPEMENT'] )
    infolist.append( arbre['properties']['SOUS_CATEGORIE_DESC'] )
    infolist.append( arbre['properties']['SOUS_CATEGORIE'] )
    infolist.append( arbre['geometry']['coordinates'][0] )
    infolist.append( arbre['geometry']['coordinates'][1] )

    arbres.append( infolist )

    print( k, end='\r' )

print( '  done  ' )

cursor.executemany("""INSERT INTO arbres VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,? )""", arbres)

db.commit()


db.close()
