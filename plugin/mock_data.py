import json

def search_restaurants(json_args):
    param = json.loads(json_args)
    query = param["query"]

    return [
        {
            "name": f"{query} レストラン1",
            "address": "東京都渋谷区",
            "rating": 4.5,
            "price_range": "¥¥¥",
            "link": "https://example.com/restaurant/1"
        },
        {
            "name": f"{query} レストラン2",
            "address": "東京都新宿区",
            "rating": 4.0,
            "price_range": "¥¥",
            "link": "https://example.com/restaurant/2"
        }
    ]

def make_reservation(json_args):
    param = json.loads(json_args)
    restaurant_id = param["restaurant_id"]
    date = param["date"]
    time = param["time"]
    party_size = param["party_size"]

    return {
        "restaurant_id": restaurant_id,
        "date": date,
        "time": time,
        "party_size": party_size,
        "reservation_status": "予約完了",
        "confirmation_number": "123456"
    }
