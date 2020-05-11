import requests
import mysql.connector



def send_data_satelitte_boat (data_to_be_send_to_the_boat):
    
    data_to_be_send_to_the_boat = data_to_be_send_to_the_boat.encode("utf-8").hex()
    url = "https://rockblock.rock7.com/rockblock/MT"
    querystring = {"imei":"69300434064048850","username":"olivier.masset.om@gmail.com","password":"Quiqsurf47","data":data_to_be_send_to_the_boat}
    response = requests.request("POST", url, params=querystring)
    print(response.text)
    


def should_we_send_new_positions_to_the_boat():
    try :
        #Connection to MySql to collect all the id of the mails already readed.
        cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
        commande = "SELECT * from update_positions;"
        cursor = cnx.cursor()
        add_data = (commande)
        # Insert new data by executing the cursor
        cursor.execute(add_data)
        question_update = cursor.fetchall()[0][1]
        # If the data has been deleted by the user, there is an error. So 'except script runs'
        cursor.close()
        cnx.close()
        return "do_not_update"
         
    except :
        

        cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')

        commande = "insert into update_positions(id,state)  values ('1','Updated');"
        #print(commande)
        cursor = cnx.cursor()
        cursor.execute(commande)
        emp_no = cursor.lastrowid
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        return 'yes we should send'



def get_next_positions_from_database ():
    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
    commande = "SELECT * FROM new_record;"
    cursor = cnx.cursor()
    add_data = (commande)
    # Insert new data by executing the cursor
    cursor.execute(add_data)
    next_positions = cursor.fetchall()
    cursor.close()
    cnx.close()
    data_to_be_send_to_the_boat = ""
    for char in next_positions :
        data_to_be_send_to_the_boat += str(char[0]) +" "+ str(char[2]) + " "+str(char[3]+ " ")
        
    return data_to_be_send_to_the_boat
    
    
if should_we_send_new_positions_to_the_boat() == 'yes we should send':
    data_to_be_send_to_the_boat = get_next_positions_from_database ()
    send_data_satelitte_boat(data_to_be_send_to_the_boat)
    
