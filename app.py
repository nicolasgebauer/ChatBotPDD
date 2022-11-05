import requests
from flask import Flask, jsonify, request
import json
import api

TOKEN = '5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto'
api_url = 'https://apipds4.herokuapp.com/'
# https://api.telegram.org/bot5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto/setWebhook?url=https://pdd-games.herokuapp.com
app = Flask(__name__)


def welcome_message(item):
    print(item)

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
        if api.create_user(user_id, username, chat_id):     
            msg = f"Usuario {username} creado con exito, bienvenid@!"
        else:
            msg = f"Error al crear usuario"
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML'
        resp = requests.get(to_url)

def set_numbers(item):
    print(item)
    sets = item["text"].split()
    chat_id = item["chat"]["id"]
    try:
        if sets[0].lower() == "numbers" and int(sets[1]) > 0 and int(sets[2]) > 0:
            msg = f"Welcome to de game Numbers >>> max = {sets[1]} intentos = {sets[2]}"
            user_id = item["from"]["id"]
            username = item["from"]["first_name"]
            final_msg = f'{msg}'

            to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
            resp = requests.get(to_url)
    except:
        final_msg = f'Sintax error to set numbers'
        to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={final_msg}&parse_mode=HTML'
        resp = requests.get(to_url)

@app.route("/", methods = ['GET','POST'])
def hello_word():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if "message" in data:
            data = data["message"]
            welcome_message(data)
            set_numbers(data)
            create_user(data)
            return {"statusCode": 200, "body": "Success", "data": data}
        else:        
            return {'satatusCode':404, 'body':'User has left the chatroom and deleted the chat', 'data':data}
    else:
        return {'satatusCode':200, 'body':'Success'}

if __name__ == '__main__':
    app.run(debug=True)