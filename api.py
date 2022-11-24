import random
import requests
import json
import unicodedata

api_url = 'https://apipds4.herokuapp.com/'
trivia_url = "https://the-trivia-api.com/api/questions?categories=general_knowledge,geography,sport_and_leisure,science,history&limit=1&difficulty=medium"

def get_new_question():
    question_data = requests.get(trivia_url)
    first_question = question_data.json()[0]
    dict_trivia = {
        "question": first_question["question"],
        "correctAnswer": fix_string(first_question["correctAnswer"]),
        "incorrectAnswers": first_question["incorrectAnswers"]
    }
    return dict_trivia

def fix_string(bad_str):
    new_str = bad_str.strip()
    new_str = unicodedata.normalize("NFKD", new_str)
    return new_str

def get_question_data(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())[0]
    options = [game["correct_answer"], game["incorrect_answer_1"], game["incorrect_answer_2"], game["incorrect_answer_3"]]
    random.shuffle(options)
    opt = {}
    for i in range(4):
        opt[chr(97+i)]=options[i] 
    data_return = {
        "question": game["question"],
        "options": options,
        "opt": opt
    }
    return data_return

def create_user(tel_id, username, lobby_id):
    data = {"username": username, "telegram_id": tel_id, "lobby": lobby_id, "won_number": 0, "won_trivia": 0, "won_third": 0, "number_tries": 0, "trivia_score": 0}
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
    active_number_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    active_trivia_first_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    print("Activos Number:", list(active_number_games.json()))
    print("activos trivia first:", list(active_trivia_first_games.json()))
    if len(list(active_number_games.json())) > 0 or len(list(active_trivia_first_games.json())) > 0:
        return 2 ## ya existe
    response = requests.post(f'{api_url}game_numbers/', json=data)
    print("CREACION DE JUEGO:", response.content)
    if response.status_code == 200:
        user_tries = set_user_tries(lobby_id, tries)
        if not user_tries:
            return 4
        return 1
    return 3

def create_trivia_first(lobby_id, question_number):
    print("numero  preguntas:", question_number)
    question = get_new_question()
    data = {
        "lobby": lobby_id,
        "questions_number": question_number,
        "status": 0, 
        "correct_answer": question["correctAnswer"],
        "incorrect_answer_1": question["incorrectAnswers"][0],
        "incorrect_answer_2": question["incorrectAnswers"][1],
        "incorrect_answer_3": question["incorrectAnswers"][2],
        "question": question["question"],
        "actual_question": 0
    }
    data_check = {"lobby_id": lobby_id}
    active_number_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    active_trivia_first_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    print("Activos Number:", list(active_number_games.json()))
    print("activos trivia first:", list(active_trivia_first_games.json()))
    if len(list(active_number_games.json())) > 0 or len(list(active_trivia_first_games.json())) > 0:
        print("result: ACA 2##########################################")
        return 2 ## ya existe
    response = requests.post(f'{api_url}game_trivia_firsts/', json=data)
    print("CREACION DE JUEGO:", response.content, response.status_code)
    if response.status_code == 200:
        if set_users_points_trivia(lobby_id):
            return 1
    return 3

def guess_number(lobby_id, guess):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    game = list(active_games.json())
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
            data = {"lobby":game[0]["lobby"], "number":game[0]["number"], "status":1}
            response = requests.put(f'{api_url}game_numbers/{game[0]["id"]}/', json=data)
            print("CAMBIO DE STATUS:", response.content)
            if response.status_code == 200:
                return 1
            return -1
    else:
        return -1

def guess_trivia_first(lobby_id, tel_id,guess):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())
    if len(game) > 0:
        print("guess:", guess)
        print("game:", game)
        correct = game[0]["correct_answer"].lower()
        print("correct:",correct)
        if guess == correct:
            print("ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            if trivia_points(lobby_id,tel_id):
                print("ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2")
                question_numbers = game[0]["questions_number"]
                if question_numbers > 1:
                    print("ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3")
                    return 1
                return 2
            return -1
    else:
        return -1
    
def set_user_tries(lobby_id, tries):
    data = {'lobby_id': lobby_id, 'tries': tries}
    response = requests.post(f'{api_url}set_users_number_tries/', params=data)
    print("CAMBIO DE INTENTOS TODOS LOS USUARIOS:", response.content)
    if response.status_code == 200:
        return True
    return False

def get_game_numbers_active(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    game = list(active_games.json())
    if len(game) > 0:
        return True
    return False

def get_game_trivia_first_active(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())
    if len(game) > 0:
        return True
    return False

def tries_down(lobby_id, tel_id):
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check)
    user = list(users.json())[0]
    print("USER:",user)
    user_id = user["id"]
    data = {
        "username": user["username"],
        "telegram_id": user["telegram_id"],
        "lobby": user["lobby"],
        "won_number": user["won_number"],
        "won_trivia": user["won_trivia"],
        "won_third": user["won_third"],
        "number_tries": (user["number_tries"]-1),
        "trivia_score": user["trivia_score"]
    }
    print("USER DATA:",data)
    response = requests.put(f'{api_url}users/{user_id}/', json=data)
    print("RESTA DE INTENTOS:", response.content)
    if response.status_code == 200:
        return True
    return False

def user_numbers_tries(lobby_id, tel_id):
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check)
    user = list(users.json())[0]
    return user["number_tries"]
    
def won_number_games(lobby_id, tel_id):
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check)
    user = list(users.json())[0]
    print("USER:",user)
    user_id = user["id"]
    data = {
        "username": user["username"],
        "telegram_id": user["telegram_id"],
        "lobby": user["lobby"],
        "won_number": user["won_number"]+1,
        "won_trivia": user["won_trivia"],
        "won_third": user["won_third"],
        "number_tries": user["number_tries"],
        "trivia_score": user["trivia_score"] 
    }
    print("USER DATA:",data)
    response = requests.put(f'{api_url}users/{user_id}/', json=data)
    print("RESTA DE INTENTOS:", response.content)
    if response.status_code == 200:
        return True
    return False

def trivia_points(lobby_id,tel_id):
    data_check1 = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check1)
    user = list(users.json())[0]
    print("USER:",user)
    user_id = user["id"]
    data = {
        "username": user["username"],
        "telegram_id": user["telegram_id"],
        "lobby": user["lobby"],
        "won_number": user["won_number"],
        "won_trivia": user["won_trivia"],
        "won_third": user["won_third"],
        "number_tries": user["number_tries"],
        "trivia_score": (user["trivia_score"] + 1)
    }
    print("USER DATA:",data)
    response = requests.put(f'{api_url}users/{user_id}/', json=data)
    print("SUBIR TRIVIA SCORE:", response.content)
    if response.status_code == 200:
        return True
    return False

def check_total_tries(lobby_id):
    data_check = {"lobby_id": lobby_id}
    total = requests.get(f'{api_url}get_tries_per_lobby/', data_check)
    print("INTENTOS TOTALES:", total.json())
    if total.json() > 0:
        return True
    return False

def end_game_numbers(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gamenumber_active/', data_check)
    game = list(active_games.json())    
    data = {"lobby":game[0]["lobby"], "number":game[0]["number"], "status":1}
    response = requests.put(f'{api_url}game_numbers/{game[0]["id"]}/', json=data)
    print("CAMBIO DE STATUS:", response.content)
    if response.status_code == 200:
        return game[0]["number"]
    return False

def get_stats(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_stat_lobby/', data_check)
    print("ORDEN DE JUGADORES:", response.content)
    in_order = "Estadisticas Number:"
    count = 0
    if response.status_code == 200:
        gamers = response.json()
        for item in gamers:
            in_order += f"""%0A    {count+1}- {item["username"]}: {item["won_number"]} ganados"""
            count += 1
        return in_order
    return False

def get_trivia_stats(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_trvia_stat_lobby/', data_check)
    print("ORDEN DE JUGADORES:", response.content)
    in_order = "Estadisticas Trivia:"
    count = 0
    if response.status_code == 200:
        gamers = response.json()
        for item in gamers:
            in_order += f"""%0A    {count+1}- {item["username"]}: {item["won_trivia"]} ganados"""
            count += 1
        return in_order
    return False

def end_game_trivia_first(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())[0]
    
    data = {
        "lobby": game["lobby"],
        "questions_number": game["questions_number"],
        "status": 1,
        "correct_answer": game["correct_answer"],
        "incorrect_answer_1": game["incorrect_answer_1"],
        "incorrect_answer_2": game["incorrect_answer_2"],
        "incorrect_answer_3": game["incorrect_answer_3"],
        "question": game["question"],
        "actual_question": game["actual_question"]
    }
    response = requests.put(f'{api_url}game_trivia_firsts/{game["id"]}/', json=data)
    print("CAMBIO DE STATUS:", response.content)
    if response.status_code == 200:
        return True
    return False

def next_question_game_trivia_first(lobby_id):
    data_check = {"lobby_id": lobby_id}
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())[0]
    print("Game ==>",game)
    new_question = get_new_question()
    new_qn = (game["questions_number"]-1)
    print("new_qn==>",new_qn)
    data = {
        "lobby": game["lobby"],
        "questions_number": new_qn,
        "status": game["status"],
        "correct_answer": new_question["correctAnswer"],
        "incorrect_answer_1": new_question["incorrectAnswers"][0],
        "incorrect_answer_2": new_question["incorrectAnswers"][1],
        "incorrect_answer_3": new_question["incorrectAnswers"][2],
        "question": new_question["question"],
        "actual_question": (game["actual_question"]+1)
    }
    response = requests.put(f'{api_url}game_trivia_firsts/{game["id"]}/', json=data)
    active_games = requests.get(f'{api_url}gametriviafirst_active/', data_check)
    game = list(active_games.json())[0]
    print("Game ==>",game)
    print("response==>",response)
    print("CAMBIO DE STATUS:", response.content)
    if response.status_code == 200:
        return game["actual_question"]
    return False

def set_users_points_trivia(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.post(f'{api_url}set_users_trivia_score_zero/', params=data_check)
    print("Trivia score zero:", response.content)
    if response.status_code == 200:
        return True
    return False

def stats_per_trivia(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_trivia_stats/', data_check)
    print("ORDEN DE JUGADORES:", response.content)
    in_order = "Estadisticas Trivia First:"
    count = 0
    if response.status_code == 200:
        gamers = response.json()
        for item in gamers:
            in_order += f"""%0A    {count+1}- {item["username"]}: {item["trivia_score"]} puntos"""
            count += 1
        in_order += f"""%0A    GANADOR DE LA TRIVIA {gamers[0]["username"]} CON {gamers[0]["trivia_score"]} PUNTOS"""
        if won_trivia_games(lobby_id,gamers[0]["telegram_id"]):
            return in_order
    return False

def won_trivia_games(lobby_id,tel_id):
    data_check = {"tel_id": tel_id, "lobby_id": lobby_id}
    users = requests.get(f'{api_url}user_created/', data_check)
    user = list(users.json())[0]
    print("USER:",user)
    user_id = user["id"]
    data = {
        "username": user["username"],
        "telegram_id": user["telegram_id"],
        "lobby": user["lobby"],
        "won_number": user["won_number"],
        "won_trivia": user["won_trivia"]+1,
        "won_third": user["won_third"],
        "number_tries": user["number_tries"],
        "trivia_score": user["trivia_score"] 
    }
    print("USER DATA:",data)
    response = requests.put(f'{api_url}users/{user_id}/', json=data)
    print("RESTA DE INTENTOS:", response.content)
    if response.status_code == 200:
        return True
    return False

def get_all_lobbies():
    response = requests.get(f'{api_url}get_all_lobbies/')
    if response.status_code == 200:
        return response.json()
    return False

def get_total_stats_per_lobby(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_total_stats_per_lobby/', data_check)
    if response.status_code == 200:
        return response.json()
    return False

def get_number_stats_per_lobby(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_stat_lobby/', data_check)
    if response.status_code == 200:
        return response.json()
    return False

def get_trivia_stats_per_lobby(lobby_id):
    data_check = {"lobby_id": lobby_id}
    response = requests.get(f'{api_url}get_trvia_stat_lobby/', data_check)
    if response.status_code == 200:
        return response.json()
    return False