from typing import List

from yandex_places import YandexPlaces


class ScoreCalculator:

    def __init__(self,
                 api_key: str,
                 ll: tuple):
        self.api_connector = YandexPlaces(api_key)
        self.ll = ll

    def request_places(self,
                       place_types: List):
        requested_places = {place: self.api_connector.get_request(self.ll,
                                                                  text=place) for place in place_types}
        requested_places["ll"] = self.ll
        return requested_places

    def request_default(self):
        return self.request_places(["Metro station", "Public transport stop",
                                    "Grocery", "Gym", "School", "Kindergarten",
                                    "University", "Cafe", "Restaurant", "Bar", "Cinema",
                                    "Theater", "Park", "Pharmacy"])


    # Grocery 5
    # Public transport stop 4.5
    # Metro station 4
    # School 3.5 3
    # Kindergarden 3
    # Park 3
    # Pharmacy 2.5
    # University 2
    # Gym 1.5
    # Restaurant 1.2
    # Cafe 1.1
    # Pub 1
    # Cinema 0.8
    # Theater 0.5

