"""

AUTHOR: Juanjo

DATE: 07/02/2019

"""

import requests


class AEMETError(Exception):
    pass


class AEMETClient:
    """
    A class representing the AEMET API entry point. Every request to the
    API is done programmatically via a concrete instance of this class.

    The class provides methods for different API endpoints.

    :param str api_key: API key to get access to AEMET API
    :returns: an *AEMETClient* instance

    """

    CONVENTIONAL_OBSERVATION_URL = 'https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{}'

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_conventional_observation(self, station_id):
        """
        Returns weather information for conventional observation.

        :param station_id: The id of the station from which gets the data
        :raises: *AEMETError* if there are any problems during the request.
        :return: a dict with weather info
        """

        url = self.CONVENTIONAL_OBSERVATION_URL.format(station_id)
        querystring = {'api_key': self.api_key}
        headers = {
            'cache-control': 'no-cache'
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
        except requests.exceptions.RequestException as re:
            raise AEMETError('An error ocurred fetching conversational observation', re)
        if response.status_code != 200:
            raise AEMETError(response.text)
        data = response.json()
        # Retrieve the temporary URL from which to request the data
        data_url = data['datos']
        try:
            response = requests.get(data_url)
        except requests.exceptions.RequestException as re:
            raise AEMETError('An error ocurred fetching conversational observation data', re)
        if response.status_code != 200:
            raise AEMETError(response.text)
        return response.json()


if __name__ == '__main__':
    # Example of use
    API_KEY = 'YOUR API KEY'
    STATION_ID = 'ID OF THE STATION'
    aemet_client = AEMETClient(API_KEY)
    conv_observation = aemet_client.fetch_conventional_observation(STATION_ID)
    last_observation = conv_observation[-1]
    # Date
    print('Date: {}'.format(last_observation['fint']))
    # Max. temperature
    print('Max Temperature: {}'.format(last_observation['tamax']))
