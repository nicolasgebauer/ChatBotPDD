import requests
from flask import Flask, jsonify, request
import json

TOKEN = "5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto"

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])

def hello_word():
    if request.method == "POST":
        data = request.get_json()
        print(f"DATA: {data}")
        return {'satatusCode':200, 'body':'Success', 'data':data}
    else:
        return {'satatusCode':200, 'body':'Success'}

if __name__ == "__main__":
    app.run(debug=True)