import logging

import requests


class WattpadAPI:
    def __init__(self):
        self.base_url = 'https://www.wattpad.com'
        self.querystring = {'offset': '0', 'limit': '100'}
        self.payload = ''
        self.headers = {'User-Agent': ''}

        self.logger = logging.getLogger('discord.wattpad.api')

    def get_user_data(self, user_name: str):
        url = self.base_url + f'/api/v3/users/{user_name}'
        try:
            response = requests.request("GET", url, data=self.payload, headers=self.headers, params=self.querystring)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(str(e))
            return None

    def get_stories_data(self, user_name: str):
        url = self.base_url + f'/v4/users/{user_name}/stories/published'
        try:
            response = requests.request("GET", url, data=self.payload, headers=self.headers, params=self.querystring)
            response.raise_for_status()
            data = response.json()
            return data['stories']
        except requests.exceptions.RequestException as e:
            self.logger.error(str(e))
            return None

    def get_message_data(self, user_name: str):
        url = self.base_url + f'/v4/users/{user_name}/messages'
        try:
            response = requests.request("GET", url, data=self.payload, headers=self.headers, params=self.querystring)
            response.raise_for_status()
            data = response.json()
            return data['messages']
        except requests.exceptions.RequestException as e:
            self.logger.error(str(e))
            return None
