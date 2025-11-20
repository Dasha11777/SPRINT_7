import requests
import allure
from data.URL import url, orders_list_endpoint
from data.order_data import generation_new_order_data

class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    @allure.description('Получение списка заказов (код - 200 и "orders" в ответе)')
    def test_get_list_of_orders(self):

        payload = generation_new_order_data("BLACK")
        requests.post(f"{url}{orders_list_endpoint}", json=payload)

        r = requests.get(f"{url}{orders_list_endpoint}")
        assert r.status_code == 200
        assert 'orders' in r.json()