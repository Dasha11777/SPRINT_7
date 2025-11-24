import requests
import allure
from data.URL import orders_list_endpoint
from data.order_data import generation_new_order_data
from data.responses import status_code_ok

class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    def test_get_list_of_orders(self):
        payload = generation_new_order_data("BLACK")
        with allure.step('Создание заказа для проверки списка'):
            requests.post(f"{orders_list_endpoint}", json=payload)

        with allure.step('Получение списка заказов'):
            r = requests.get(f"{orders_list_endpoint}")
            assert r.status_code == status_code_ok
            assert 'orders' in r.json()