import requests
import allure
from data.order_data import generation_new_order_data, order_colors
import pytest
from data.URL import orders_list_endpoint
from data.responses import status_code_created

class TestCreateOrder:

    @pytest.mark.parametrize('color', order_colors)
    @allure.title('Создание заказа')
    def test_create_order(self, color):
        payload = generation_new_order_data(color)
        with allure.step('Создание заказа'):
            r = requests.post(f"{orders_list_endpoint}", json=payload)
            assert r.status_code == status_code_created
            assert 'track' in r.json()