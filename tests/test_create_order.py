import requests
import allure
from data.order_data import generation_new_order_data
import pytest
from data.URL import url, orders_list_endpoint

class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])
    @allure.title('Создание заказа')
    @allure.description('Проверка создания заказа (код - 201 и track в ответе)')
    def test_create_order(self, color):
        payload = generation_new_order_data(color)
        r = requests.post(f"{url}{orders_list_endpoint}", json=payload)
        assert r.status_code == 201
        assert 'track' in r.json()