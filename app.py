import requests
from flask import Flask, jsonify, request
import json

TOKEN = '5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto'

app = Flask(__name__)


def welcome_message(item):
    print(item)

    if item["text"].lower() == "hi":
        msg = "hello"
        chat_id = item['chat']['id']
        user_id = item["from"]["id"]
        username = item['from']["username"]
        welcome_msg = f'{msg} {username}'

        to_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={welcome_msg}&parse_mode=HTML"
        resp = requests.get(to_url)


@app.route("/", methods = ['GET','POST'])
def hello_word():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if "message" in data:
            data = data["message"]
            welcome_message(data)
            return {"statusCode": 200, "body": "Success", "data": data}
        else:        
            return {'satatusCode':404, 'body':'User has left the chatroom and deleted the chat', 'data':data}
    else:
        return {'satatusCode':200, 'body':'Success'}

if __name__ == '__main__':
    app.run(debug=True)