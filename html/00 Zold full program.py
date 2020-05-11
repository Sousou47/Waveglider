from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import json
import datetime, time


###############################################################
# Data received from RFM
# I will send this date line per line. It's easier to be exploited.
#      date   latitude    longitude    temperature sensor

# Decalage
DIR = '2 142.45789 -94.098753 3 59.45789 10.753 4 -90.45789 210.753 5 12 -10 '
# changement pos
#DIR = '1 142.45789 -94.098753 2 59.45789 10.753 3 -90.45789 210.753 4 12 -10 '



#RFM = '2020 03 15 20 58 44.04 -0.009735 20.6 3 '
#RFM = '2020 03 18 12 59 43.3 -84.9 15.3 5 '
#RFM = '2020 03 22 22 21 41.41 2.09 16.12 3 '
RFM = '2020 03 25 10 25 55.86 -4.28 10.89 8 '
#RFM = '2020 03 29 02 51 31.13 29.93 6.35 7 '
#RFM = '2020 03 31 18 04 10.45 10.75 5.74 9 '
#RFM = '2020 04 02 19 12 40.4 -3.7 10.68 10 '
#RFM = '2020 04 05 15 31 54.31 10.09 7.54 4 '

input = 0

################################################################
def insert_data (database, table, date, dat2, latitude, longitude):
    cnx = mysql.connector.connect(user='Olivier', password = 'password',  database=database)
    print(dat2)
    commande = "insert into " + table + '(date,dat2,latitude, longitude) VALUES (' + date + ',' + str(dat2) + ',' + latitude + ',' + longitude + ')'
    print(commande)
    
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

    print("date")
    
    d = int(translate_date (dico_data["datey"],dico_data["datem"],dico_data["dated"],dico_data["dateh"],dico_data["datemi"]))
    print("date",d)
    t = float(dico_data["temperature"])
    data["price_usd"] = data["price_usd"]+[[d,t]]
    print(data)

    with open('./releves_temperatures.json', 'w') as json_file:
      json.dump(data, json_file)
  
  
  
def add_json_ph(dico_data):
    with open('./Sensors_pH.json') as f:
      data = json.load(f)

    print("date")
    
    d = int(translate_date (dico_data["datey"],dico_data["datem"],dico_data["dated"],dico_data["dateh"],dico_data["datemi"]))
    print("date",d)
    t = float(dico_data["ph"])
    data["ph"] = data["ph"]+[[d,t]]
    print(data)

    with open('./Sensors_pH.json', 'w') as json_file:
      json.dump(data, json_file)
  
  
  

################################################################
######### Modifying directions  ##########
      
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




##########################################

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


################################################################
## Run script



if input == 0 :

    dico_data = data_rfmchc_to_dictionnary (RFM)
    add_json_temperatures(dico_data)
    add_json_ph(dico_data)
    print(dico_data)
    #print(dico_directions(DIR))
    insert_data('register', "last_locations" , dico_data['date'],dico_data['dat2'], dico_data['latitude'], dico_data['longitude'])
  
if input == 1 :
        
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
