import requests
import pytest
import allure
from data.URL import url, login_courier_endpoint, delete_courier_endpoint
from data.courier_data import register_new_courier_and_return_login_password_name

@pytest.fixture
def delete_courier_data():
    login_pass_name = register_new_courier_and_return_login_password_name()
    yield {
        "login": login_pass_name[0],
        "password": login_pass_name[1]
    }
    response = requests.post(f"{url}{login_courier_endpoint}", data=login_pass_name)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}{delete_courier_endpoint}/{courier_id}")


class TestLoginCourier:
    @allure.title('Авторизация курьера')
    @allure.description('Проверка получения ID курьера при авторизации с корректным login и password (код - 200 и ID')
    def test_get_courier_id(self, delete_courier_data):
        payload = delete_courier_data
        response = requests.post(f"{url}{login_courier_endpoint}", data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Авторизация курьера не пройдена при отправке неверного password')
    @allure.description('Проверка отправки неверного password при автроизации курьера (код - 404 и "message": "Учетная запись не найдена"')
    def test_get_courier_id(self):
        login_pass_name = register_new_courier_and_return_login_password_name()
        
        payload = {
            "login": login_pass_name[0],
            # используем неверный пароль (логин вместо пароля)
            "password": login_pass_name[0]
        }
        response = requests.post(f"{url}{login_courier_endpoint}", data=payload)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}, "Неверное содержимое ответа."

    @allure.title('Авторизация курьера не пройдена при отправке не всех обязательных полей')
    @allure.description(
        'Проверка авторизации курьера без обязательного поля - password (код - 400 и "message": ""message":  "Недостаточно данных для входа"')
    def test_login_courier_without_password(self):
        login_pass_name = register_new_courier_and_return_login_password_name()
        payload = {
            "login": login_pass_name[0],
            "password": ""
        }
        response = requests.post(f"{url}{login_courier_endpoint}", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}