import json
from typing import List, Tuple, Union

from tgbot.config import Config
from tgbot.services.api_requests import request_to_api


async def parse_cities_group(city: str, config: Config) -> Union[List[Tuple], None]:
    url = config.misc.url_search
    querystring = {"q": city, "locale": "ru_RU"}

    headers = {
        "X-RapidAPI-Key": config.misc.api_key,
        "X-RapidAPI-Host": config.misc.api_host
    }

    response = await request_to_api(url, headers=headers, querystring=querystring, method='GET')
    if response:
        cities = list()
        try:
            result = json.loads(response.text)
            for place in result.get('sr'):
                if place.get('type') in ['CITY', 'NEIGHBORHOOD']:
                    city = place.get('regionNames').get('primaryDisplayName')
                    description = place.get('regionNames').get('secondaryDisplayName')
                    city_id = place.get('gaiaId')
                    cities.append((city, description, city_id))
        except Exception:
            cities = None
        return cities
    return None
