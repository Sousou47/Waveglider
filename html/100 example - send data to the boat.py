import requests

data_to_be_send_to_the_boat = "rtyui"

def send_data_satelitte_boat (data_to_be_send_to_the_boat):
    data_to_be_send_to_the_boat = data_to_be_send_to_the_boat.encode("utf-8").hex()

    url = "https://rockblock.rock7.com/rockblock/MT"

    querystring = {"imei":"69300434064048850","username":"olivier.masset.om@gmail.com","password":"Quiqsurf47","data":data_to_be_send_to_the_boat}

    response = requests.request("POST", url, params=querystring)

    print(response.text)
send_data_satelitte_boat(data_to_be_send_to_the_boat)