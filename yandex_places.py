from typing import Tuple

import requests
from cachetools import cached, TTLCache
from dist_calculator import dist_btw_coords

ttl = TTLCache(maxsize=512, ttl=86400)


class YandexPlaces:
    """
    Places is responsible fot the connection with Google Maps API
    queries
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __url_creator(self,
                      ll: Tuple,
                      text: str,
                      result: int = 25
                      ):
        url = "".join(["https://search-maps.yandex.ru/v1/?",
                       f"apikey={self.api_key}",
                       f"&text={text}",
                       "&lang=en_RU",
                       f"&ll={ll[0]},{ll[1]}",
                       f"&results={result}]"
                       ]
                      )

        return url

    @cached(cache=ttl)
    def get_request(self,
                    ll: Tuple,
                    text: str,
                    result: int = 25
                    ):
        url = self.__url_creator(ll,
                                 text,
                                 result)

        content = requests.get(url)
        places = content.json()

        for i in places["features"]:
            i["distance"] = dist_btw_coords(*ll, *i['geometry']['coordinates'])

        places["features"] = sorted(places["features"], key=lambda x: x["distance"])

        return places
