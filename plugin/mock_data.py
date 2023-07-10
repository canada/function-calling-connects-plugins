import json

def get_travel_products():
    return [
        {
            "product_page": "https://example.com/product/1",
            "image_url": "https://example.com/images/product1.jpg",
            "price": 50000,
            "destination": "大阪",
            "flights": {
                "departure": {
                    "airport": "HND",
                    "time": "2022-01-01T:00:00",
                    "flight_number": "NH123"
                },
                "return": {
                    "airport": "KIX",
                    "time": "2022-01-05T20:00:00",
                    "flight_number": "NH456"
                }
            }
        },
        {
            "product_page": "https://example.com/product/2",
            "image_url": "https://example.com/images/product2.jpg",
            "price": 55000,
            "destination": "大阪",
            "flights": {
                "departure": {
                    "airport": "NRT",
                    "time": "2022-01-01T12:00:00",
                    "flight_number": "JL789"
                },
                "return": {
                    "airport": "KIX",
                    "time": "2022-01-05T22:00:00",
                    "flight_number": "JL012"
                }
            }
        },
        {
            "EXTRA_INFORMATION_TO_ASSISTANT": "Never call this function again with the same parameters. AI and user cannot make reservation with this Plugin(function)"
        }
    ]


def get_region_overview(json_args):
    param = json.loads(json_args)

    if param["region"] == '京都':
        return {
            "region": "京都",
            "overview": "京都は歴史と文化が息づく美しい都市で、多くの寺院や神社があります。",
            "link": "https://example.com/region",
            "image_url": "https://example.com/images/region.jpg"
        }
    elif param["region"] == '東京':
        return {
            "region": "東京",
            "overview": "東京は日本の首都で、世界有数の大都市です。人口は14,090,347人（2023年6月1日現在）。これは日本の都道府県の中では人口が最も多く、日本の人口のおよそ11%を占めている。人口密度も都道府県の中で最も高い。東京都を中心とする東京都市圏は人口3700万人を超える世界最大の都市圏である。日本の人口の約3割が集中し、ポーランドやモロッコ、カナダなどの国の総人口に匹敵する。",
            "link": "https://example.com/region",
            "image_url": "https://example.com/images/region.jpg"
        }
    else:
        return {
            "region": param["region"],
            "overview": "温泉がいっぱい",
            "link": "https://example.com/region",
            "image_url": "https://example.com/images/region.jpg"
        }


def get_recommended_spots():
    return [
        {
            "name": "清水寺",
            "overview": "清水寺は、京都市東山区にある歴史ある寺院で、絶景ポイントで有名です。",
            "link": "https://example.com/spot/1",
            "image_url": "https://example.com/spot1.jpg"
        },
        {
            "name": "金閣寺",
            "overview": "金閣寺は、京都市北区にある歴史ある建造物が見どころのスポットです。",
            "link": "https://example.com/spot/2",
            "image_url": "https://example.com/images/spot2.jpg"
        }
    ]
