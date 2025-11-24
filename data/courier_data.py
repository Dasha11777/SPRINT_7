import requests
import random
import string
from data.URL import create_courier_endpoint

def generation_new_data_courier():
    letters = string.ascii_lowercase
    login_new = ''.join(random.choice(letters) for i in range(10))
    password_new = ''.join(random.choice(letters) for i in range(10))
    first_name_new = ''.join(random.choice(letters) for i in range(10))

    return {"login": login_new, "password": password_new, "firstName": first_name_new}

def register_new_courier_and_return_login_password_name():

    login_pass = []

    data = generation_new_data_courier()
    login = data["login"]
    password = data["password"]
    first_name = data["firstName"]

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{create_courier_endpoint}", data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass