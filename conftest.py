import pytest
import requests
from data.URL import delete_courier_endpoint, create_courier_endpoint, login_courier_endpoint
from data.courier_data import generation_new_data_courier, register_new_courier_and_return_login_password_name
from data.responses import status_code_created, status_code_ok

@pytest.fixture
def courier_cleanup():
    courier_ids = []
    yield courier_ids
    for courier_id in courier_ids:
        requests.delete(f"{delete_courier_endpoint}/{courier_id}")

@pytest.fixture
def create_new_courier(courier_cleanup):
    payload = generation_new_data_courier()
    response = requests.post(create_courier_endpoint, data=payload)
    
    if response.status_code == status_code_created:
        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(login_courier_endpoint, data=login_payload)
        if login_response.status_code == status_code_ok:
            courier_id = login_response.json().get("id")
            courier_cleanup.append(courier_id)
            payload['id'] = courier_id
            
    return payload

@pytest.fixture
def delete_courier_data():
    login_pass_name = register_new_courier_and_return_login_password_name()
    yield {
        "login": login_pass_name[0],
        "password": login_pass_name[1]
    }
    
    payload = {
        "login": login_pass_name[0],
        "password": login_pass_name[1],
        "firstName": login_pass_name[2]
    }
    response = requests.post(f"{login_courier_endpoint}", data=payload)
    if response.status_code == status_code_ok:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{delete_courier_endpoint}/{courier_id}")