import requests
import json

api_url = 'https://apipds4.herokuapp.com/'

def create_user(tel_id, username, lobby_id):
    data = {"telegram_id": tel_id, "username": username, "lobby": lobby_id, "won_number": 0, "won_trivia": 0, "won_third": 0, "number_tries": 0}
    response = requests.post(f'{api_url}users/', data)
    if response.status_code == 200:
        print(response.content)
        return True
    return False