import requests
import json

api_url = 'https://apipds4.herokuapp.com/'

def create_user(tel_id, username, lobby_id):
    data = {"telegram_id": tel_id, "username": username, "lobby": lobby_id}
    response = requests.post(f'{api_url}users/', json=data)
    if response.status_code == 200:
        print(response.content)
        return True
    return False