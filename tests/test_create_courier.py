import requests
import allure
import pytest
from data.URL import url, create_courier_endpoint, login_courier_endpoint, delete_courier_endpoint
from data.courier_data import generation_new_data_courier
from data.courier_data import register_new_courier_and_return_login_password_name

@pytest.fixture
def registered_courier_data():
    login_pass_name = register_new_courier_and_return_login_password_name()
    return {
        "login": login_pass_name[0],
        "password": login_pass_name[1],
        "firstName": login_pass_name[2]
    }

class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и текст - "ok": True')
    def test_create_courier(self):
        payload = generation_new_data_courier()

        response = requests.post(f"{url}/{create_courier_endpoint}", data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."

        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f"{url}{login_courier_endpoint}", data=login_payload)
        assert login_response.status_code == 200, "Login failed."

        courier_id = login_response.json().get("id")
        assert courier_id is not None, "Courier ID not found in login response."

        # Delete the created courier
        delete_response = requests.delete(f"{url}{delete_courier_endpoint}/{courier_id}")
        assert delete_response.status_code == 200, "Failed to delete courier."

    @allure.title('Проверка невозможности создать курьера. дублирующие креды')
    @allure.description('Проверка, что нельзя создать курьера с уже существующеми кредами (код - 409 и текст - "message": "Этот логин уже используетсяПопробуйте другой."')
    def test_create_courier_duplicate_login(self, registered_courier_data):
        payload = registered_courier_data
        response = requests.post(f"{url}{create_courier_endpoint}", data=payload)

        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}, "Неверное содержимое ответа."

    @allure.title('Проверка невозможности создать курьера. Не все обязательные поля')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 400 и текст - "message": "Недостаточно данных для создания учетной записи"')
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }
        response = requests.post(f"{url}{create_courier_endpoint}", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}, "Неверное содержимое ответа."