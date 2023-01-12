import requests as req
from requests.auth import HTTPBasicAuth
import json
import sys
import os
import logging as log


token_logger = log.getLogger(__name__)
token_logger.setLevel(log.INFO)
log_file_handler = log.FileHandler('./logs/auth_logs.log')
log_format = log.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
log_file_handler.setFormatter(log_format)
token_logger.addHandler(log_file_handler)


class TokenOperations:
    def __init__(self, settings, char_name):
        self.settings = settings
        self.char_name = char_name
        self.refresh_token = ''
        self.auth_params = HTTPBasicAuth(settings['client_id'], settings['client_secret'])
        self.directory = './user_data/'
        self.files = os.listdir(self.directory)

    def token_update(self, by_command_line=None):
        if f'{self.char_name}_token_info.json' in self.files:
            with open(f'{self.directory}{self.char_name}_token_info.json', 'r') as f:
                content = json.load(f)
                self.refresh_token = content["refresh_token"]
            refresh_auth = req.post('https://login.eveonline.com/v2/oauth/token',
                                    auth=self.auth_params,
                                    data={'grant_type': 'refresh_token',
                                          'refresh_token': {self.refresh_token}}
                                    )
            if refresh_auth.status_code == 200:
                new_token = refresh_auth.json()['access_token']
                content["refresh_token"] = refresh_auth.json()['refresh_token']
                content["access_token"] = new_token
                with open(f'{self.directory}{self.char_name}_token_info.json', 'w') as f:
                    json.dump(content, f, indent=2)
                token_logger.info(f'{self.char_name} token updated')
                if by_command_line:
                    print(refresh_auth.status_code, '- token updated!')
                    print("Token file is updated!")
                return new_token
            else:
                if by_command_line:
                    print(refresh_auth.status_code, '- error')
                token_logger.error(f'{self.char_name} token update error - {refresh_auth.status_code}')
                sys.exit('Error with token update!')
        else:
            print(f'No character with this name - {self.char_name}')
