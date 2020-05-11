import mysql.connector

# Decalage
DIR = '2 142.45789 -94.098753 3 59.45789 10.753 4 -90.45789 210.753 5 12 -10 '
# changement pos
#DIR = '1 142.45789 -94.098753 2 59.45789 10.753 3 -90.45789 210.753 4 12 -10 '



def dico_directions(DIR) :

    chc = ''
    dico_donnees_directions = {}

    compteur = 0
    for a in DIR :
        
        if a == ' ':
              compteur += 1
              #print("compteur", compteur)
              if compteur == 1 :
                id = chc
                #print(id)
                chc = ''
              elif compteur == 2 :
                latitude = chc
                #print(latitude)
                chc = ''
              elif compteur == 3 :
                longitude = chc
                #print(longitude)
                chc = ''
                compteur = 0
                dico_donnees_directions[int(id)] = [float(latitude),float(longitude)]
              
        else :
            
             chc += a
    return dico_donnees_directions





def dico_futures_positions():
    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
    commande = "SELECT * FROM new_record;"
    cursor = cnx.cursor()
    add_data = (commande)
    # Insert new data by executing the cursor
    cursor.execute(add_data)
    next_positions = cursor.fetchall()
    cursor.close()
    cnx.close()

    dico_futures_positions = {}
    for a in next_positions :
        dico_futures_positions[a[0]] = [a[2],a[3]]
    return dico_futures_positions




dico_futures_positions = dico_futures_positions()
dico_directions = dico_directions(DIR)
print("dico_futures_positions", dico_futures_positions)


difference = False
for a in range(0,5) :
    try :
        if (dico_directions[a] != int(dico_futures_positions[a])):
            difference = True
    except :
        azerty = 1

print("dico_directions", dico_directions)

if difference == True :
    dico_directions = dico_futures_positions
else :
    decrementation = 0
    try :
        dico_directions[0]
        # Everything is corresponding; we don't do anything.
    except :
        try :
            dico_directions[1]
            decrementation = 0
        except :
            try :
                dico_directions[2]
                decrementation = 1
            except :
                try :
                    dico_directions[3]
                    decrementation = 2
                except :
                    azerty = 1
    
    if decrementation != 0 :
        for a in range(1,5) :
            try :
                dico_futures_positions[a] = dico_directions[a+decrementation]
            except :
                azerty = 1


    else :
        dico_directions = dico_futures_positions
    
    

print("dico_directions boat", dico_directions)
print("dico_futures_positions webserver", dico_futures_positions)


##############################################################################################
##Now I will clear all the Database, and incorporate all the new positions.###################


cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')

# First, delete everything of the table
commande = "DELETE FROM new_record;"
cursor = cnx.cursor()
add_data = (commande)
# Insert new data by executing the cursor
cursor.execute(add_data)
cnx.commit()





# Now, insert data from dictionnary

for a in dico_futures_positions :
    commande = "insert into new_record (id,latitude,longitude) VALUES ("+str(a)+","+str(dico_futures_positions[a][0])+","+str(dico_futures_positions[a][1])+");"


    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')

    cursor = cnx.cursor()
    add_data = (commande)
    # Insert new data by executing the cursor
    cursor.execute(add_data)
    cnx.commit()



cursor.close()
cnx.close()



#### New record :

"""
|  1 | 0000-00-00 00:00:00 | 49.45789  | -4.098753  |             |
|  2 | 0000-00-00 00:00:00 | 142.45789 | -94.098753 |             |
|  3 | 0000-00-00 00:00:00 | 59.45789  | 10.753     |             |
|  4 | 0000-00-00 00:00:00 | -90.45789 | 210.753    |             |
|  5 | 2020-04-06 12:59:53 | 12        | -10        | olivier


insert into new_record (id,latitude,longitude) VALUES (1,49,4.45);
"""