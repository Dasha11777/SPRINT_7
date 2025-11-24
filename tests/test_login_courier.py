import requests
import allure
from data.URL import login_courier_endpoint, delete_courier_endpoint
from data.courier_data import register_new_courier_and_return_login_password_name
from data.responses import login_courier_not_found, login_courier_missing_data, status_code_ok, status_code_not_found, status_code_bad_request

class TestLoginCourier:
    @allure.title('Авторизация курьера')
    def test_get_courier_id(self, delete_courier_data):
        payload = delete_courier_data
        with allure.step('Авторизация курьера'):
            response = requests.post(f"{login_courier_endpoint}", data=payload)

            assert response.status_code == status_code_ok
            assert 'id' in response.json()

    @allure.title('Авторизация курьера не пройдена при отправке неверного password')
    def test_login_courier_wrong_password(self):
        login_pass_name = register_new_courier_and_return_login_password_name()
        
        payload = {
            "login": login_pass_name[0],
            # используем неверный пароль (логин вместо пароля)
            "password": login_pass_name[0]
        }
        with allure.step('Попытка авторизации с неверным паролем'):
            response = requests.post(f"{login_courier_endpoint}", data=payload)

            assert response.status_code == status_code_not_found
            assert response.json() == login_courier_not_found, "Неверное содержимое ответа."

    @allure.title('Авторизация курьера не пройдена при отправке не всех обязательных полей')
    def test_login_courier_without_password(self):
        login_pass_name = register_new_courier_and_return_login_password_name()
        payload = {
            "login": login_pass_name[0],
            "password": ""
        }
        with allure.step('Попытка авторизации без пароля'):
            response = requests.post(f"{login_courier_endpoint}", data=payload)

            assert response.status_code == status_code_bad_request
            assert response.json() == login_courier_missing_data