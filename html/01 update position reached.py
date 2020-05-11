import mysql.connector



def delete_position_webserver_1 ():
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


    decrementation = 1
    for a in range(1,5) :
        try :
            dico_futures_positions[a] = dico_futures_positions[a+decrementation]
        except :
            azerty = 1


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
    
    
delete_position_webserver_1 ()
