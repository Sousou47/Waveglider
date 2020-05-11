#waveglidereps@gmail.com
#glidereps
#https://developers.google.com/gmail/api/quickstart/python

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import json
import datetime, time

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import email

import requests

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


# The main objective of this function is to read mails, see if there is a new one, extract its content and say if a position is reached.
def read_new_mail():


    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    messages = service.users().messages().list(userId='me').execute()

    #print('Messages into INBOX : ',messages)
    #print(messages['messages'])
    #service.users().messages().delete(userId='me', id='171c11f0832986e5').execute()

    #Connection to MySql to collect all the id of the mails already readed.
    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
    commande = "SELECT * FROM mails_readed;"
    cursor = cnx.cursor()
    add_data = (commande)
    # Insert new data by executing the cursor
    cursor.execute(add_data)
    mails_readed = cursor.fetchall()
    #print(mails_readed)
    cursor.close()
    cnx.close()
    
    
    for message in messages['messages']:

        ## The idea is to check if the ID of this message is not already registered into MYSQL. Else, it has already been readed.
        ID_exists = False
        for id_messages in mails_readed :

            if id_messages[0] == str(message['id']) :
                ID_exists = True
        if ID_exists == False : 
            message = service.users().messages().get(userId='me', id=str(message['id']),format='raw').execute()
            clean_message = message['snippet']
            print('new mail')
            
            
            ######## The mail will be treated. I put its ID to avoid another treatment further
            cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
            commande = "insert into mails_readed values ('"+str(message['id'])+"')"
            #print(commande)
            cursor = cnx.cursor()
            cursor.execute(commande)
            emp_no = cursor.lastrowid
            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            cnx.close()
            #################################

            if clean_message[0:4] == 'IMEI' :
                print('MESSAGE COMPLET : ', clean_message)
                for a in range(0,len(clean_message)):
                    if(clean_message[a:a+5] == 'Time:'):
                        chaine_caracteres = clean_message[a+6:a+10] + " " + clean_message[a+11:a+13] + " " + clean_message[a+14:a+16]+ " " + clean_message[a+17:a+19] + " " + clean_message[a+20:a+22] + " "
                    if(clean_message[a] == '$'):
                        chaine_caracteres += clean_message[a+1:len(clean_message)+1]+' '
                        return('data_pos_sensors',chaine_caracteres)
                    if(clean_message[a] == '£'):
                        chaine_caracteres += clean_message[a+1:len(clean_message)+1]+' '
                        return('positionR', chaine_caracteres)
            



infos_bateau = read_new_mail()
print(infos_bateau)

try :
    if infos_bateau[0] == 'data_pos_sensors':
        input = "onlydata"
        RFM = infos_bateau[1]

    if infos_bateau[0] == 'positionR' :
        input = "dataandpositionreached"
        RFM = infos_bateau[1]
except :
    input = "no new mails"




###############################################################
# Data received from RFM
# I will send this date line per line. It's easier to be exploited.
#      date   latitude    longitude    temperature sensor

# Decalage
#DIR = '2 142.45789 -94.098753 3 59.45789 10.753 4 -90.45789 210.753 5 12 -10 '
# changement pos
#DIR = '1 142.45789 -94.098753 2 59.45789 10.753 3 -90.45789 210.753 4 12 -10 '



#RFM = '2020 03 15 20 58 44.04 -0.009735 20.6 3 '
#RFM = '2020 03 18 12 59 43.3 -84.9 15.3 5 '
#RFM = '2020 03 22 22 21 41.41 2.09 16.12 3 '
#RFM = '2020 03 25 10 25 55.86 -4.28 10.89 8 '
#RFM = '2020 03 29 02 51 31.13 29.93 6.35 7 '
#RFM = '2020 03 31 18 04 10.45 10.75 5.74 9 '
#RFM = '2020 04 02 19 12 40.4 -3.7 10.68 10 '
#RFM = '2020 04 05 15 31 54.31 10.09 7.54 4 '


################################################################
def insert_data (database, table, date, dat2, latitude, longitude):
    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database=database)
    #print(dat2)
    commande = "insert into " + table + '(date,dat2,latitude, longitude) VALUES (' + date + ',' + str(dat2) + ',' + latitude + ',' + longitude + ')'
    #print(commande)
    
    cursor = cnx.cursor()

    add_data = (commande)

    # Insert new data by executing the cursor
    cursor.execute(add_data)
    emp_no = cursor.lastrowid


    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    
    
################################################################
######### Take RFM data and put it into a dictionnary ##########
    
def data_rfmchc_to_dictionnary (RFM) :
    data = ''
    liste2 = ["datey","datem","dated","dateh","datemi", "latitude", "longitude", "temperature", "ph"]
    liste = []
    dico_data = {}
    rang = 0
    for a in RFM :
        if a != " "  :
            data += a
        else :
            liste+= [data]
            dico_data[liste2[rang]] = data
            rang +=1
            data = ""
            if rang == 7 :
                dico_data["date"] = dico_data["datey"]+''+dico_data["datem"]+''+dico_data["dated"]+''+dico_data["dateh"]+''+dico_data["datemi"]
                dico_data["dat2"] = str(dico_data["datey"])+''+str(dico_data["datem"])+''+str(dico_data["dated"])+''+str(dico_data["dateh"])+''+str(dico_data["datemi"])

            
            
    rang = 0
    liste = []
    #print(dico_data)
    return dico_data


######### Take RFM data and put it into a dictionnary ##########
################################################################
def translate_date (yyyy,mm,dd,hh,mi):
    d = datetime.datetime(int(yyyy),int(mm),int(dd),int(hh),int(mi))
    for_js = int(time.mktime(d.timetuple())) * 1000
    return for_js


################################################################
######### Add data into Json file ##########

def add_json_temperatures(dico_data):
    with open('./releves_temperatures.json') as f:
      data = json.load(f)

    #print("date")
    
    d = int(translate_date (dico_data["datey"],dico_data["datem"],dico_data["dated"],dico_data["dateh"],dico_data["datemi"]))
    #print("date",d)
    t = float(dico_data["temperature"])
    data["price_usd"] = data["price_usd"]+[[d,t]]
    #print(data)

    with open('./releves_temperatures.json', 'w') as json_file:
      json.dump(data, json_file)
  
  
  
def add_json_ph(dico_data):
    with open('./Sensors_pH.json') as f:
      data = json.load(f)

    #print("date")
    
    d = int(translate_date (dico_data["datey"],dico_data["datem"],dico_data["dated"],dico_data["dateh"],dico_data["datemi"]))
    #print("date",d)
    t = float(dico_data["ph"])
    data["ph"] = data["ph"]+[[d,t]]
    #print(data)

    with open('./Sensors_pH.json', 'w') as json_file:
      json.dump(data, json_file)
  
  
  

################################################################
######### Modifying directions  ##########
      
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
    
 

##########################################
################################################################
################################################################
# This part is used to send the next positions to the boat if the user asks on the web page
    
def send_data_satelitte_boat (data_to_be_send_to_the_boat):
    
    data_to_be_send_to_the_boat = data_to_be_send_to_the_boat.encode("utf-8").hex()
    url = "https://rockblock.rock7.com/rockblock/MT"
    querystring = {"imei":"69300434064048850","username":"olivier.masset.om@gmail.com","password":"Quiqsurf47","data":data_to_be_send_to_the_boat}
    response = requests.request("POST", url, params=querystring)
    print(response.text)
    


def should_we_send_new_positions_to_the_boat():
    

    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
    commande = "SELECT * from update_positions;"
    
    
    cursor = cnx.cursor()
    add_data = (commande)
    # Insert new data by executing the cursor
    cursor.execute(add_data)
    try : 
        question_update = cursor.fetchall()[0][1]
        #print(mails_readed)
        cursor.close()
        cnx.close()

        return 'do_not_update'
    except :
        cursor.close()
        cnx.close()
        cnx = mysql.connector.connect(user='Olivier', password = 'password',  database='register')
        commande = "insert into update_positions(id,state)  values ('1','do_not_update');"
        #print(commande)
        cursor = cnx.cursor()
        cursor.execute(commande)
        emp_no = cursor.lastrowid
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        return 'yes_we_should_send'




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


# Script associated
if should_we_send_new_positions_to_the_boat() == 'yes_we_should_send':
    print('the user asked to change the new positions to the boat')
    data_to_be_send_to_the_boat = get_next_positions_from_database ()
    send_data_satelitte_boat(data_to_be_send_to_the_boat)
else :
    print( 'the user did not ask to send the next positions to the boat')

################################################################
################################################################
################################################################
## Run script

print(input)

if input == "onlydata" or input == "dataandpositionreached" :

    dico_data = data_rfmchc_to_dictionnary (RFM)
    add_json_temperatures(dico_data)
    add_json_ph(dico_data)
    print(dico_data)
    #print(dico_directions(DIR))
    insert_data('register', "last_locations" , dico_data['date'],dico_data['dat2'], dico_data['latitude'], dico_data['longitude'])
    if input == "dataandpositionreached" :
        delete_position_webserver_1 ()

    ##############################################################################################
    ##Now I will clear all the Database, and incorporate all the new positions.###################




################################################################
################## GPS Data ####################################

"""
Coordonnées groupe de travail
2019 12 30 20 58 44.04 -0.009735 20
2020 01 09 42 59 43.3 -84.9 15
2020 03 22 22 21 41.41 2.09 16
2020 03 25 10 25 55.86 -4.28 10
2020 03 29 02 51 31.13 29.93 6
2020 03 31 18 04 10.45 10.75 5
2020 03 31 19 12 40.4 -3.7 10
2020 04 02 15 31 54.31 10.09 7
"""


################################################################
################## SQL Commands ################################

"""
sudo mysql;
show databases;
use resister;
show tables;
select * from last_locations;
drop table last_locations;

"""

################## SQL Commands ################################
################################################################

"""
{'price_usd': 
[[1581007954111, -2.98], 
[1583329554111, 30.18], 
[1584007954111, 6.98], 
[1586007954111, 2.98], 
[1589007954111, 20.98]]}

"""


