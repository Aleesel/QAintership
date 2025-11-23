from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_item, get_items, get_stats, post_item,delete_item
from assertions.assertion_base import assert_status_code, assert_response_body_fields, assert_schema
from models.object_models import ItemData, StatsData, NullItemData, CreateItemData
from utilities.files_utils import read_json_common_request_data

unic_sellerId = 753162
null_sellerId = 946842
incorrect_sellerId = 'sellerId'
item_UUID = '661597a0-eb5f-4c2e-846b-c18215d5d9af'
incorrect_item_UUID = '661597a0-eb5f-4c2e-846b-c18215d111af'

#Тесты для проверки Get методов по Id товара
class TestItem:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_item(self, client, request):
        """
        получение заранее заготовленного товара из базы,
        GET /api/1/item/{}
        """

        # получаем товар с сервера
        response = get_item(client, item_UUID)

        # убеждаемся, что получен именно тот товар, который мы запросили
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ItemData)
        assert_response_body_fields(request, response)

    def test_get_item_not_exist_id(self, client, request):
        """
        попытка получить из базы товар с несуществующим id,
        GET /api/1/item/{}
        """
        # пытаемся получить товар, несуществующий в системе
        response = get_item(client, incorrect_item_UUID)

        # убеждаемся, что в ответ пришел not found
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_response_body_fields(request, response)

    def test_get_item_invalid_id(self, client, request):
        """
        попытка получить из базы товар с невалидным по типу id,
        GET /api/1/item/{}
        """
        # пытаемся получить объект, отправив невалидный по типу параметр ids
        response = get_item(client, 23321)

        # убеждаемся, что в ответ пришел bad request
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_response_body_fields(request, response)

#Тесты для проверки Get методов по SellerId продавца
class TestItems:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()


    def test_get_items(self, client, request):
        """
        получение заранее заготовленных товаров из базы по sellerId,
        GET /api/1/{}/item
        """
        # получаем объекты из базы
        response = get_items(client, unic_sellerId)

        # убеждаемся, что в ответ пришли объекты, которые мы ожидаем
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body_fields(request, response)

    def test_get_items_not_exist_id(self, client, request):
        """
        попытка получить из базы товары с несуществующим sellerId,
        GET /api/1/{}/item
        """
        # пытаемся получить объект, несуществующий в системе
        response = get_items(client, 946842)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body_fields(request, response)

    def test_get_items_invalid_id(self, client, request):
        """
        попытка получить из базы товары с невалидным по типу sellerId,
        GET /api/1/{}/item
        """
        # пытаемся получить объект, отправив невалидный по типу параметр ids
        response = get_item(client, incorrect_sellerId)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_response_body_fields(request, response)


#Тесты для проверки Get методов статистики по id товара
class TestStatistics:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_stats(self, client, request):
        """
        получение статистики по id товара,
        GET /api/1/statistic/{}
        """

        # получаем единичный объект с сервера
        response = get_stats(client, item_UUID)

        # убеждаемся, что получен именно тот объект, который мы запросили
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, StatsData)
        assert_response_body_fields(request, response)

    def test_get_stats_not_exist_id(self, client, request):
        """
        попытка получить из базы статистики по несуществующему id товара,
        GET /api/1/statistic/{}
        """
        # пытаемся получить объект, несуществующий в системе
        response = get_stats(client, incorrect_item_UUID)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_response_body_fields(request, response)

    def test_get_stats_invalid_id(self, client, request):
        """
        попытка получить из базы статистики с невалидным по типу id товара,
        GET /api/1/statistic/{}
        """
        # пытаемся получить объект, отправив невалидный по типу параметр ids
        response = get_stats(client, 23321)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_response_body_fields(request, response)


#Тесты для проверки Post методов создания товара
class TestPost:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_post_item_empty_body(self, client, request):
        """
        запись товара в базу с пустым телом,
        POST /api/1/item
        """
        # записываем объект в базу с пустым телом
        response = post_item(client, json={})

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_schema(response, NullItemData)
        assert_response_body_fields(request, response)

    def test_post_item_with_full_body(self, client, request):
        """
        запись товара в базу полностью заполненным телом,
        POST /api/1/item
        и последующим удалением товара,
        DELETE /api/2/item/{}
        """
        # записываем объект в базу со всеми заполненными полями
        exp_obj = read_json_common_request_data("valid_post_object")
        response = post_item(client, json=exp_obj)

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, CreateItemData)

        response_delete = delete_item(client, response.json()["status"][23:])
        assert_status_code(response_delete, HTTPStatus.OK)


    def test_post_item_send_invalid_json(self, client, request):
        """
        попытка записать в базу товара с невалидным json,
        POST /api/1/item
        """
        # отправляем запрос на запись объекта в базу с невалидным json в теле
        response = post_item(client, content='{"sellerID": "invalid_string", "name": "Test Item", "price": 1000, "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}', headers={"Content-Type": "application/json"})

        # убеждаемся, что сервер дал BAD REQUEST ответ
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_response_body_fields(request, response)

    def test_post_item_with_invalid_price(self, client, request):
        """
        запись товара в базу с отрицательной ценой,
        POST /api/1/item
        и последующим удалением товара,
        DELETE /api/2/item/{}
        """
        # записываем объект в базу со всеми заполненными полями
        exp_obj = read_json_common_request_data("invalid_price_post_object")
        response = post_item(client, json=exp_obj)

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, CreateItemData)

        response_delete = delete_item(client, response.json()["status"][23:])
        assert_status_code(response_delete, HTTPStatus.OK)

    def test_post_item_with_max_price(self, client, request):
        """
        запись товара в базу с выходящим за рамки integer значением цены,
        POST /api/1/item
        """
        # записываем объект в базу со всеми заполненными полями
        exp_obj = read_json_common_request_data("max_price_post_object")
        response = post_item(client, json=exp_obj)

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_schema(response, CreateItemData)