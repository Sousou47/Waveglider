
import mysql.connector


cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')

# First, delete everything of the table
commande = "DELETE FROM new_record;"
cursor = cnx.cursor()
print(cursor)
add_data = (commande)
print(add_data)
print(cursor)
# Insert new data by executing the cursor
cursor.execute(add_data)
print(cursor)




   # Make sure data is committed to the database
cnx.commit()
    
    
cursor.close()
cnx.close()