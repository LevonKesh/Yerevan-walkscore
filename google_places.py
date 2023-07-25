import requests


class GooglePlaces:
    """
    Places is responsible fot the connection with Google Maps API
    queries
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __url_creator(self,
                      lat: float,
                      long: float,
                      type_: str = "",
                      keyword: str = "",
                      radius: int = 1500,
                      rankby: str = "prominence"
                      ):

        if rankby == "distance":
            rad_par = ""
        else:
            rad_par = f"radius={radius}&"

        if type_ == keyword == "":
            raise ValueError("Both type_ and keyword for search are not set")

        url = "".join(["https://maps.googleapis.com/maps/api/place/nearbysearch/json?",
                       f"location={lat},{long}&",
                       f"keyword={keyword}&",
                       rad_par,
                       f"type={type_}&",
                       f"rankby={rankby}&",
                       f"key={self.api_key}"
                       ]
                      )

        return url

    def get_request(self,
                    lat: float,
                    long: float,
                    type_: str = "",
                    keyword: str = "",
                    radius: int = 1500,
                    rankby: str = "prominence"
                    ):

        url = self.__url_creator(lat,
                                 long,
                                 type_,
                                 keyword,
                                 radius,
                                 rankby)


        content = requests.get(url)

        return content.json()
