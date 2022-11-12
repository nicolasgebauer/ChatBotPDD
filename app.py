import requests
from flask import Flask, jsonify, request
import json
import api

TOKEN = '5716588187:AAH_kxlWI2GGSbmHEAANh53CGgvOfkBfNWM'
api_url = 'https://apipds4.herokuapp.com/'
# https://api.telegram.org/bot5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto/setWebhook?url=https://pdd-games.herokuapp.com
# https://api.telegram.org/bot5716588187:AAH_kxlWI2GGSbmHEAANh53CGgvOfkBfNWM/setWebhook?url=https://pdd-games.herokuapp.com
app = Flask(__name__)

def welcome_message(item):
    if item["text"].lower() == "info":
        msg = "Hay tres juegos:\n"
        msg += "1)NUMBERS: Conciste en adivinar el número seleccionado por el bot.\n"
        msg += "    Este Juego se inicia con el mensaje => Numbers 'max' 'intentos'.\n"
        msg += "    Max => Número maximo que puede seleccionar el bot.\n"
        msg += "    Intentos => Intentos por jugador.\n"
        chat_id = item["chat"]["id"]
        username = item["from"]["first_name"]
        welcome_msg = f'{msg}'

        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={welcome_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def create_user(item):
    if item["text"].lower() == "/start":
        user_id = str(item["from"]["id"])
        username = str(item["from"]["first_name"])
        chat_id = item["chat"]["id"]
        chat_id_str = str(chat_id)
        msg = ""
        user = api.create_user(user_id, username, chat_id_str)
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
    chat_id_str = str(chat_id)
    if api.get_game_numbers_active(chat_id_str):
        set_guess(item)

def set_numbers(item):
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    try:
        if sets[0].lower() == "numbers" and int(sets[1]) > 0 and int(sets[2]) > 0:
            game = api.create_number_game(chat_id_str, int(sets[1]), int(sets[2]))
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
    chat_id_str = str(chat_id)
    user_id = str(item["from"]["id"])
    username = item["from"]["first_name"]
    error = False
    msg_error = ""
    try:
        if sets.isnumeric() and api.user_numbers_tries(chat_id_str,user_id) > 0:
            game = api.guess_number(chat_id_str, int(sets))
            msg = ""
            if game == 1:
                if api.won_number_games(chat_id, user_id):
                    msg_correct_number_guessed = f"Correcto el numero es {sets}."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_correct_number_guessed}&parse_mode=HTML'
                    resp = requests.get(to_url)
                    msg_congratulations_message = f"Felicitaciones {username} eres el ganador."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_congratulations_message}&parse_mode=HTML'
                    resp = requests.get(to_url)
                    msg_end_game = "Juego finalizado."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_end_game}&parse_mode=HTML'
                    resp = requests.get(to_url)
                else:
                    msg_error = "Error al subir los juegos numbers ganados."
                    error = True
            elif game == 2:
                if api.tries_down(chat_id_str,user_id):
                    tries = api.user_numbers_tries(chat_id_str,user_id)
                    msg_upper_number_guess = f"El numero es mayor a {sets}."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_upper_number_guess}&parse_mode=HTML'
                    resp = requests.get(to_url)
                    msg_rest_tries = f"{username} te quedan {tries} intentos."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_rest_tries}&parse_mode=HTML'
                    resp = requests.get(to_url)
                    if not api.check_total_tries(chat_id_str):
                        end_gme = api.end_game_numbers(chat_id_str)
                        if end_gme != False:
                            msg_game_losers = f"Juego terminado, ya no quedan más intentos."
                            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_game_losers}&parse_mode=HTML'
                            resp = requests.get(to_url)
                            msg_end = f"El numero correcto era: {end_gme}"
                            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_end}&parse_mode=HTML'
                            resp = requests.get(to_url)
                        else:
                            msg_error = "Error al terminar juego"
                            error = True
                else:
                    msg_error = "Error al bajar los intentos"
                    error = True
            elif game == 3:
                if api.tries_down(chat_id_str,user_id):
                    tries = api.user_numbers_tries(chat_id_str,user_id)
                    msg_lower_number_guess = f"El numero es menor a {sets}."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_lower_number_guess}&parse_mode=HTML'
                    resp = requests.get(to_url)
                    msg_rest_tries = f"{username} te quedan {tries} intentos."
                    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_rest_tries}&parse_mode=HTML'
                    resp = requests.get(to_url)                                        
                    if not api.check_total_tries(chat_id_str):
                        end_gme = api.end_game_numbers(chat_id_str)
                        if end_gme != False:
                            msg_game_losers = f"Juego terminado, ya no quedan más intentos."
                            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_game_losers}&parse_mode=HTML'
                            resp = requests.get(to_url)
                            msg_end = f"El numero correcto era: {end_gme}"
                            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_end}&parse_mode=HTML'
                            resp = requests.get(to_url)
                        else:
                            msg_error = "Error al terminar juego"
                            error = True
                else:
                    msg_error = "Error al bajar los intentos"
                    error = True
            else:
                msg_error = "Error al intentar jugada un juego."
                error = True
        if error:
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_error}&parse_mode=HTML'
            resp = requests.get(to_url)
                
    except:
        final_msg = f'Error de sintaxis en jugada.'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def stats(item):
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    if item["text"].lower() == "stats":
        result = api.get_stats(chat_id_str)
        if  result != False:
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={result}&parse_mode=HTML'
            resp = requests.get(to_url)
        else:
            msg = "Error al conseguir las estadísticas."
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)

def set_trivia_first(item):
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    try:
        if sets[0].lower() == "trivia" and sets[1].lower() == "first" and int(sets[2]) > 0:
            game = api.create_trivia_first(chat_id_str, int(sets[2]))
            msg = ""
            if game[0] == 1:
                question = game[1]
                incorrect = game[2]
                correct = game[3]
                msg_good = f"Juego Trivia: First, iniciado >>> preguntas = {sets[2]}."
                send_msg(chat_id, msg_good)
                msg_question = f"Pregunta 1: {question}"
                send_msg(chat_id, msg_question)
                msg = f"{incorrect}, {correct}"
            elif game[0] == 2:
                msg = "Ya existe un juego activo."
            else:
                msg = "Error al crear un juego."
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)
    except:
        final_msg = f'Error de sintaxis para creación de juego.'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def send_msg(chat_id, msg):
    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
    resp = requests.get(to_url)

@app.route("/", methods = ['GET','POST'])
def hello_word():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if "message" in data:
            data = data["message"]
            print(data)
            if "text" in data:
                welcome_message(data)
                set_numbers(data)
                set_trivia_first(data)
                is_game_numbers_active(data)
                create_user(data)
                stats(data)
                return {"statusCode": 200, "body": "Success", "data": data}
            else:        
                return {'statusCode':404, 'body':'User has left the chatroom and deleted the chat', 'data':data}
        else:
            return {'statusCode':200, 'body':'Success'}
    return

if __name__ == '__main__':
    app.run(debug=True)