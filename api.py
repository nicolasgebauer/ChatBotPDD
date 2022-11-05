import requests
import json

api_url = 'https://apipds4.herokuapp.com/'

def create_user(tel_id, username, lobby_id):
    data = {"username": username, "telegram_id": tel_id, "lobby": lobby_id, "won_number": 0, "won_trivia": 0, "won_third": 0, "number_tries": 0}
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    usuarios = requests.get(f'{api_url}user_created/', data_check)
    print("Usuarios:", usuarios.content)
    if len(list(usuarios.content)) > 0:
        return 2 ## ya existe
    #response = requests.post(f'{api_url}users/', json=data)
    #print(response.content)
    #if response.status_code == 200:
    #    print(response.content)
    #    return 1
    return 3  ## error server