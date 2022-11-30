import requests
from flask import Flask, jsonify, request, render_template
import json
import api
import urllib
import math_game


TOKEN = '5716588187:AAH_kxlWI2GGSbmHEAANh53CGgvOfkBfNWM'
api_url = 'https://apipds4.herokuapp.com/'
stats_link = "https://pdd-games.herokuapp.com/stats"
# https://api.telegram.org/bot5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto/setWebhook?url=https://pdd-games.herokuapp.com
# https://api.telegram.org/bot5716588187:AAH_kxlWI2GGSbmHEAANh53CGgvOfkBfNWM/setWebhook?url=https://pdd-games.herokuapp.com
app = Flask(__name__)

def welcome_message(item):
    if item["text"].lower() == "info":
        msg = "Hay tres juegos:\n"
        msg += "1)NUMBERS: Consiste en adivinar el número seleccionado por el bot.\n"
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

def is_game_trivia_first_active(item):
    chat_id = item["chat_id"]
    chat_id_str = str(chat_id)
    if api.get_game_trivia_first_active(chat_id_str):
        set_guess_trivia_first(item)

def is_game_math_active(item):
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    if api.get_game_math_active(chat_id_str):
        set_math_guess(item)

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
        total = api.get_total_stats(chat_id_str)
        result_1 = api.get_numbers_stats(chat_id_str)
        result_2 = api.get_trivia_stats(chat_id_str)
        result_3 = api.get_third_stats(chat_id_str)
        msg = f"Para mas detalles ingrese al link.\n{stats_link}"
        if  result_1 != False and result_2 != False and result_3 != False and total != False:
            send_msg(chat_id, total)
            send_msg(chat_id, result_1)
            send_msg(chat_id, result_2)
            send_msg(chat_id, result_3)
            send_msg(chat_id, msg)
        else:
            msg = "Error al conseguir las estadísticas."
            send_msg(chat_id, msg)

def set_trivia_first(item):
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    try:
        if sets[0].lower() == "trivia" and sets[1].lower() == "first" and int(sets[2]) > 0:
            game = api.create_trivia_first(chat_id_str, int(sets[2]))
            print("GAME: ",game)
            msg = ""
            if game == 1:
                q_data = api.get_question_data(chat_id_str)
                question = q_data["question"]
                options = q_data["options"]
                msg_good = f"Juego Trivia: First, iniciado >>> preguntas = {sets[2]}."
                send_msg(chat_id, msg_good)
                msg_question = f"Pregunta 1: {question}"
                send_msg(chat_id, msg_question)
                print("options:", options)
                keyboard = setKeyboard(options)
                print("keyboard after json:",keyboard)
                msg_options = ""
                for i in range(len(options)):
                   msg_options += f"{chr(i+97)}) {options[i]}\n"
                sendTextWithButtons(chat_id, msg_options, keyboard)
            elif game == 2:
                msg = "Ya existe un juego activo."
            else:
                msg = "Error al crear un juego."
            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
            resp = requests.get(to_url)
    except:
        final_msg = f'Error de sintaxis para creación de juego.'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def set_guess_trivia_first(item):
    sets = str(item["text"])
    chat_id = item["chat_id"]
    chat_id_str = str(chat_id)
    user_id = str(item["user_id"])
    username = item["username"]
    error = False
    msg_error = ""
    try:
        guess = sets.lower()
        #if guess == "a" or guess == "b" or guess == "c" or guess == "d":
        q_data = api.get_question_data(chat_id_str)
        question = q_data["question"]
        options = q_data["options"]
        game = api.guess_trivia_first(chat_id_str, user_id, sets.lower())
        print("game-->",game)
        if game == 1:
            msg = f"Respuesta {sets} es correcta, {username}"
            send_msg(chat_id,msg)
            next_q = api.next_question_game_trivia_first(chat_id_str)
            if next_q != False:
                q_data = api.get_question_data(chat_id_str)
                question = q_data["question"]
                options = q_data["options"]
                msg_question = f"Pregunta {next_q+1}: {question}"
                send_msg(chat_id, msg_question)
                keyboard = setKeyboard(options)
                print("keyboard after json:",keyboard)
                msg_options = ""
                for i in range(len(options)):
                   msg_options += f"{chr(i+97)}) {options[i]}\n"
                sendTextWithButtons(chat_id, msg_options, keyboard)
        elif game ==2:
            msg = f"Respuesta {sets} es correcta, {username}"
            send_msg(chat_id,msg)
            if api.end_game_trivia_first(chat_id_str):
                msg = f"Juego terminado."
                send_msg(chat_id,msg)
                stats = api.stats_per_trivia(chat_id_str)
                if  stats != False:
                    send_msg(chat_id,stats)
            else:
                msg = f"Error al terminar juego."
                send_msg(chat_id,msg)
    except:
        msg = f"Respuesta NO recibida, {username}"
        send_msg(chat_id,msg)

def set_math(item):
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    result, operation = math_game.create_math_games_params()
    print(operation)
    try:
        if sets[0].lower() == "math" and len(sets) == 1:
            game = api.create_math(chat_id_str, operation, result)
            operation = operation.replace("+","%s+")
            msg = ""
            msg2 = f"'{operation}'"
            if game == 1:
                msg = f"Juego math iniciado >>> resolver:"
                send_msg(chat_id, msg)
                send_msg(chat_id, "+")
                send_msg(chat_id, msg2)
                
            elif game == 2:
                msg = "Ya existe un juego activo."
                send_msg(chat_id, msg)
            else:
                msg = "Error al crear un juego."
                send_msg(chat_id, msg)
            
    except:
        final_msg = f'Error de sintaxis para creación de juego.'
        send_msg(chat_id, final_msg)

def set_math_guess(item):
    sets = str(item["text"])
    chat_id = item["chat"]["id"]
    chat_id_str = str(chat_id)
    user_id = str(item["from"]["id"])
    username = item["from"]["first_name"]
    error = False
    msg_error = ""
    try:
        if math_game.is_negative_number_digit(sets):
            game = api.guess_math_result(chat_id_str, int(sets))
            msg = ""
            if game == 1:
                if api.won_third_game(chat_id_str, user_id):
                    msg_correct_number_guessed = f"Correcto el resultado es {sets}."
                    send_msg(chat_id, msg_correct_number_guessed)
                    msg_congratulations_message = f"Felicitaciones {username} eres el ganador."
                    send_msg(chat_id, msg_congratulations_message)
                    msg_end_game = "Juego finalizado."
                    send_msg(chat_id, msg_end_game)
                else:
                    msg_error = "Error al subir los juegos math ganados."
                    error = True
            elif game == 2:
                msg_upper_number_guess = f"El resultado es mayor a {sets}."
                send_msg(chat_id, msg_upper_number_guess)
            elif game == 3:
                msg_lower_number_guess = f"El resultado es menor a {sets}."
                send_msg(chat_id, msg_lower_number_guess)
            else:
                msg_error = "Error al intentar jugada un juego."
                error = True
        if error:
            send_msg(chat_id, msg_error)
                
    except:
        final_msg = f'Error de sintaxis en jugada.'
        send_msg(chat_id, final_msg)

def send_msg(chat_id, msg):
    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
    print(to_url)
    resp = requests.get(to_url)

@app.route("/", methods = ['GET','POST'])
def hello_word():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if 'callback_query' in data:
            print(f'ES CALLBACK QUERY')
            data = {
                "text": data["callback_query"]["data"],
                "chat_id": data["callback_query"]["message"]["chat"]["id"],
                "user_id": data["callback_query"]["from"]["id"],
                "username": data["callback_query"]["from"]["first_name"]              
            }
            is_game_trivia_first_active(data)
        if "message" in data:
            data = data["message"]
            print(data)
            if "text" in data:
                welcome_message(data)
                set_numbers(data)
                set_trivia_first(data)
                set_math(data)
                is_game_numbers_active(data)
                is_game_math_active(data)
                create_user(data)
                stats(data)
                return {"statusCode": 200, "body": "Success", "data": data}
            else:        
                return {'statusCode':404, 'body':'User has left the chatroom and deleted the chat', 'data':data}
        else:
            return {'statusCode':200, 'body':'Success'}
    return

@app.route("/stats")
def total_stats():
    lobbies = api.get_all_lobbies()
    c = 1
    total_data = {}
    numbers_data = {}
    trivia_data = {}
    third_data = {}
    for lobby in lobbies:
        total_data[c] = api.get_total_stats_per_lobby(lobby)
        numbers_data[c] = api.get_number_stats_per_lobby(lobby)
        trivia_data[c] = api.get_trivia_stats_per_lobby(lobby)
        third_data[c] = api.get_third_stats_per_lobby(lobby)
        c += 1
    return render_template("stats.html", total_data=total_data, numbers_data = numbers_data, trivia_data = trivia_data, third_data = third_data)

def sendTextWithButtons(chat_id, answer, keyboard):
    pay_data = {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': answer,
        'reply_markup': keyboard
    }
    data = {
        'method': 'post',
        'payload': pay_data
    }
    #https://api.telegram.org/bot[TOKEN]/sendMessage?chat_id=[CHAT_ID]&text=[TEXT]&reply_markup={"inline_keyboard": [[{"text": "hi", "callback_data": "hi"}]]}
    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={answer}&reply_markup={keyboard}'
    resp = requests.get(to_url, json=data)
    print("RESPUESTA:", resp.text)

def setKeyboard(options):
    keyboard = {
        'inline_keyboard': [
            [{
                'text': 'A',
                'callback_data': options[0]
            }],
            [{
                'text': 'B',
                'callback_data': options[1]
            }],
            [{
                'text': 'C',
                'callback_data': options[2]
            }],
            [{
                'text': 'D',
                'callback_data': options[3]
            }]
        ]
    }
    print("keyboard before json:",keyboard)
    return json.dumps(keyboard)

if __name__ == '__main__':
    app.run()
