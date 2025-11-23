from enum import Enum


class Routes(str, Enum):
    ITEM_GET = '/api/1/item/{}'
    ITEM_POST = '/api/1/item'
    STATISTIC_GET = '/api/1/statistic/{}'
    SELLER_ID_ITEM_GET = '/api/1/{}/item'
    DELETE_ITEM = '/api/2/item/{}'

    def __str__(self) -> str:
        return self.value