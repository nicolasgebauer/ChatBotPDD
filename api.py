import random
import requests
import json

api_url = 'https://apipds4.herokuapp.com/'

def create_user(tel_id, username, lobby_id):
    data = {"username": username, "telegram_id": tel_id, "lobby": lobby_id, "won_number": 0, "won_trivia": 0, "won_third": 0, "number_tries": 0}
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check)
    print("Usuarios:", list(users.json()))
    if len(list(users.json())) > 0:
        return 2 ## ya existe
    response = requests.post(f'{api_url}users/', json=data)
    print("CREACION DE USUARIO:", response.content)
    if response.status_code == 200:
        return 1
    return 3  ## error server

def create_number_game(lobby_id, max_number, tries):
    rand_number = random.randint(1, max_number)
    print("numero maximo:", max_number)
    print("intentos", tries)
    data = {"lobby": lobby_id, "number": rand_number, "status": 0}
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    print("Activos:", list(active_games.json()))
    if len(list(active_games.json())) > 0:
        return 2 ## ya existe
    response = requests.post(f'{api_url}game_numbers/', json=data)
    print("CREACION DE JUEGO:", response.content)
    if response.status_code == 200:
        user_tries = set_user_tries(lobby_id, tries)
        if not user_tries:
            return 4
        return 1
    return 3

def guess_number(lobby_id, guess, user_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    rest_tries(lobby_id,user_id)
    game = list(active_games.json())
    game_id = game[0]["id"]
    if len(game) > 0:
        print("guess:", guess)
        print("game:", game)
        number = game[0]["number"]
        print("number:",number)
        if guess < number:
            return 2
        elif guess > number:
            return 3
        else:
            print("game id:",game_id)
            data = {"lobby": int(game[0]["lobby"]),"number": int(game[0]["number"]),"status": 1}
            response = requests.post(f'{api_url}set_users_number_tries/{game_id}/', params=data)
            print("CAMBIO STATUS GAME:", response)
            
            return 1
    else:
        return -1
    
def set_user_tries(lobby_id, tries):
    data = {'lobby_id': lobby_id, 'tries': tries}
    response = requests.post(f'{api_url}game_numers/', params=data)
    print("CAMBIO DE INTENTOS TODOS LOS USUARIOS:", response.content)
    if response.status_code == 200:
        return True
    return False

def rest_tries(lobby_id,user_id):
    data_check = {"tel_id": user_id, "lobby_id": lobby_id}
    user = requests.get(f'{api_url}user_created/', data_check)
    print("user:",user.json())