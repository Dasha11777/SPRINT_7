import requests
import allure
import pytest
from data.URL import create_courier_endpoint, login_courier_endpoint, delete_courier_endpoint
from data.courier_data import generation_new_data_courier
from data.responses import create_courier_success, create_courier_duplicate_login, create_courier_missing_data, status_code_created, status_code_ok, status_code_conflict, status_code_bad_request

class TestCreateCourier:

    @allure.title('Создание курьера')
    def test_create_courier(self, courier_cleanup):
        payload = generation_new_data_courier()

        with allure.step('Создание курьера'):
            response = requests.post(f"{create_courier_endpoint}", data=payload)
            assert response.status_code == status_code_created
            assert response.json() == create_courier_success, "Неверное содержимое ответа."

        with allure.step('Логин курьера для получения ID'):
            login_payload = {
                "login": payload["login"],
                "password": payload["password"]
            }
            login_response = requests.post(f"{login_courier_endpoint}", data=login_payload)
            assert login_response.status_code == status_code_ok, "Login failed."

            courier_id = login_response.json().get("id")
            assert courier_id is not None, "Courier ID not found in login response."
            courier_cleanup.append(courier_id)

    @allure.title('Проверка невозможности создать курьера. дублирующие креды')
    @allure.description('Проверка, что нельзя создать курьера с уже существующеми кредами (код - 409 и текст - "message": "Этот логин уже используетсяПопробуйте другой."')
    def test_create_courier_duplicate_login(self, create_new_courier):
        payload = {
            "login": create_new_courier["login"],
            "password": create_new_courier["password"],
            "firstName": create_new_courier["firstName"]
        }
        with allure.step('Попытка создания курьера с дублирующимися данными'):
            response = requests.post(f"{create_courier_endpoint}", data=payload)

            assert response.status_code == status_code_conflict
            assert response.json() == create_courier_duplicate_login, "Неверное содержимое ответа."

    @allure.title('Проверка невозможности создать курьера. Не все обязательные поля заполнены')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 400 и текст - "message": "Недостаточно данных для создания учетной записи"')
    @pytest.mark.parametrize('missed_field_name', ["password", "login"])
    def test_create_courier_without_password(self, missed_field_name):
        data = generation_new_data_courier()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"],
            "password": data["password"]
        }
        payload.pop(missed_field_name)

        with allure.step(f'Попытка создания курьера без {missed_field_name}'):
            response = requests.post(f"{create_courier_endpoint}", data=payload)

            assert response.status_code == status_code_bad_request
            assert response.json() == create_courier_missing_data, "Неверное содержимое ответа."