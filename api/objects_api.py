from api import routes

def get_item(client, item_id):
    return client.get(routes.Routes.ITEM_GET.format(item_id))

def get_stats(client, item_id):
    return client.get(routes.Routes.STATISTIC_GET.format(item_id))

def get_items(client, sellerId):
    return client.get(routes.Routes.SELLER_ID_ITEM_GET.format(sellerId))

def post_item(client, **kwargs):
    return client.post(routes.Routes.ITEM_POST, **kwargs)

def delete_item(client, item_id):
    return client.delete(routes.Routes.DELETE_ITEM.format(item_id))


