import requests
from flask import Flask, jsonify, request
import json
import api

TOKEN = '5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto'
api_url = 'https://apipds4.herokuapp.com/'
# https://api.telegram.org/bot5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto/setWebhook?url=https://pdd-games.herokuapp.com
app = Flask(__name__)


def welcome_message(item):
    if item["text"].lower() == "hi":
        msg = "hello"
        chat_id = item["chat"]["id"]
        user_id = item["from"]["id"]
        username = item["from"]["first_name"]
        welcome_msg = f'{msg} {username}'

        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={welcome_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def create_user(item):
    if item["text"].lower() == "create user":
        user_id = int(item["from"]["id"])
        username = str(item["from"]["first_name"])
        chat_id = int(item["chat"]["id"])
        msg = ""
        user = api.create_user(user_id, username, chat_id)
        if  user == 1:     
            msg = f"Usuario {username} creado con exito, bienvenid@!"
        elif user == 2:
            msg = f"Usuario {username} ya existe."
        else:
            msg = f"Error al crear usuario."
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def is_game_numbers_active(item):
    chat_id = item["chat"]["id"]
    if api.get_game_numbers_activate(chat_id):
        set_guess(item)


def set_numbers(item):
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    try:
        if sets[0].lower() == "numbers" and int(sets[1]) > 0 and int(sets[2]) > 0:
            game = api.create_number_game(chat_id, int(sets[1]), int(sets[2]))
            msg = ""
            if game == 1:
                msg = f"Juego Numbers iniciado >>> max = {sets[1]} intentos = {sets[2]}."
            elif game == 2:
                msg = "Ya existe un juego activo."
            elif game == 4:
                msg = "Error en cambio a los turnos."
            else:
                msg = "Error al crear un juego."
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)
    except:
        final_msg = f'Error de sintaxis para creación de juego.'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def set_guess(item):
    sets = str(item["text"])
    chat_id = item["chat"]["id"]
    user_id = int(item["from"]["id"])
    username = item["from"]["first_name"]
    try:
        if sets.isnumeric() and api.user_numbers_tries(chat_id,user_id) > 0:
            game = api.guess_number(chat_id, int(sets))
            msg = ""
            if game == 1:
                if api.won_number_games(chat_id, user_id):
                    msg = f"Correcto el numero es {sets}."
                    msg1 = f"Felicitaciones {username} eres el ganador."
                    msg2 = "Juego finalizado."
                else:
                    msg = "Error al subir los juegos numbers ganados."
            elif game == 2:
                if api.tries_down(chat_id,user_id):
                    tries = api.user_numbers_tries(chat_id,user_id)
                    msg = f"El numero es mayor a {sets}."
                    msg1 = f"{username} te quedan {tries} intentos."
                    api.check_total_tries(chat_id)
                else:
                    msg = "Error al bajar los intentos"
            elif game == 3:
                if api.tries_down(chat_id,user_id):
                    tries = api.user_numbers_tries(chat_id,user_id)
                    msg = f"El numero es menor a {sets}."
                    msg1 = f"{username} te quedan {tries} intentos."
                    api.check_total_tries(chat_id)
                else:
                    msg = "Error al bajar los intentos"
            else:
                msg = "Error al intentar jugada un juego."
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg1}&parse_mode=HTML'
            resp = requests.get(to_url)
            if game == 1:
                to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg2}&parse_mode=HTML'
                resp = requests.get(to_url)
    except:
        final_msg = f'Error de sintaxis en jugada.'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

@app.route("/", methods = ['GET','POST'])
def hello_word():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if "message" in data:
            data = data["message"]
            print(data)
            welcome_message(data)
            set_numbers(data)
            is_game_numbers_active(data)
            create_user(data)
            return {"statusCode": 200, "body": "Success", "data": data}
        else:        
            return {'satatusCode':404, 'body':'User has left the chatroom and deleted the chat', 'data':data}
    else:
        return {'satatusCode':200, 'body':'Success'}

if __name__ == '__main__':
    app.run(debug=True)