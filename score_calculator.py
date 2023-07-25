from functools import cached_property
from pathlib import Path
from typing import List

import numpy as np
import yaml

from utils.functions import distance_to_score
from yandex_places import YandexPlaces


class ScoreCalculator:

    def __init__(self,
                 api_key: str,
                 ll: tuple):
        self.api_connector = YandexPlaces(api_key)
        self.ll = ll
        self.requested_vals = None

    @cached_property
    def total_weights(self):
        with open(Path("utils", "total_weights.yaml")) as f:
            total_weights = yaml.safe_load(f)
        return total_weights

    @cached_property
    def weights(self):
        with open(Path("utils", "weights.yaml")) as f:
            weights = yaml.safe_load(f)
        return weights

    @cached_property
    def scales(self):
        with open(Path("utils", "scales.yaml")) as f:
            scales = yaml.safe_load(f)
        return scales

    def request_places(self,
                       place_types: List):
        self.requested_vals = {place: self.api_connector.get_request(self.ll,
                                                                     text=place)["features"] for place in place_types}
        return self.requested_vals

    def request_default(self):
        return self.request_places(["Metro station", "Public transport stop",
                                    "Grocery", "School", "Kindergarten",
                                    "Restaurant", "Park", "Pharmacy"])

    def value_calculator(self):
        if not self.requested_vals:
            self.request_default()
        scores = {}
        total_weight = sum(self.total_weights.values())

        for place_type in self.requested_vals:
            weight_place = np.array(self.weights[place_type])
            scaled = weight_place * 100
            vals_place = np.array([distance_to_score(i["distance"], self.scales[place_type])
                                   for i in self.requested_vals[place_type]][:len(weight_place)])
            vals_place = vals_place * weight_place
            vals_scales = 100 * (vals_place / scaled)
            scores[place_type] = (sum(vals_scales) / len(vals_scales)) * (self.total_weights[place_type] / total_weight)

        return sum(scores.values())



