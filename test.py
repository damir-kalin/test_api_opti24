import os

import requests
from dotenv import load_dotenv
import logging

URL_API = 'https://api-demo.opti-24.ru/'
URL_SITE = 'https://demo.opti-24.ru/'

class UserAPI:
    def __init__(self, login: str, pwd: str, hash_pwd: str, api_key: str, logger: logging.Logger):
        self.login = login
        self.pwd = pwd
        self.hash_pwd = hash_pwd
        self.api_key = api_key
        self.logger = logger

    def get_session(self):
        url = URL_API + 'vip/v1/authUser'
        headers = {'User-Agent': 'Mozilla/5.0', 
                   'api_key': self.api_key, 
                   'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'login': self.login, 
                  'password': self.hash_pwd}
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f'''Error get data, status-code =  {str(response.status_code)} \n
                            {response.text}
                         ''')
            return None
        
    def get_data(self, json_data):
        url = URL_API + 'vip/v1/getPartContractData'
        headers = {
            'User-Agent': 'Mozilla/5.0', 
            'api_key': self.api_key,
            'session_id': json_data['data']['session_id']
        }
        params = {
            'contract_id': json_data['data']['contracts'][0]['id']
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f'''Error get data, status-code =  {str(response.status_code)} \n
                            {response.text}
                         ''')
            return None
            



if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    load_dotenv()
    login = os.getenv('LOGIN')
    pwd = os.getenv('PWD')
    hash_pwd = os.getenv('HASH_PWD')
    api_key = os.getenv('API_KEY')
    user = UserAPI(login, pwd, hash_pwd, api_key, logger)
    json_data = user.get_session()
    print(user.get_data(json_data))
