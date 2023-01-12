import base64
import secrets
import urllib
import hashlib
import requests as req
from jose import jwt, ExpiredSignatureError
import time
import json
import os
import logging as log


auth_logger = log.getLogger(__name__)
auth_logger.setLevel(log.INFO)
log_file_handler = log.FileHandler('./logs/auth_logs.log')
log_format = log.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
log_file_handler.setFormatter(log_format)
auth_logger.addHandler(log_file_handler)


class InitCharAuth:
    def __init__(self, settings):
        self.settings = settings
        self.user_auth = {}
        self.session = req.Session()

        self.refresh_token = ''
        self.access_token = ''
        self.expired = -1

        self.character_id = ''
        self.character_name = ''
        self.resended_label_id = ''

        self.login_jwt_url = "login.eveonline.com"

        self.random = base64.urlsafe_b64encode(secrets.token_bytes(32))
        m = hashlib.sha256()
        m.update(self.random)
        d = m.digest()
        self.code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")

    def print_auth_url(self):
        base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/"
        unique_state = base64.urlsafe_b64encode(secrets.token_bytes(8)).decode().replace("=", "")
        params = {
            "response_type": "code",
            "redirect_uri": self.settings['client_callback_url'],
            "client_id": self.settings['client_id'],
            'scope': ' '.join(map(str, self.settings['scopes'])),
            "state": unique_state,
            "code_challenge": self.code_challenge,
            "code_challenge_method": "S256"
        }

        string_params = urllib.parse.urlencode(params)
        full_auth_url = f'{base_auth_url}?{string_params}'
        print(full_auth_url)
        return self.auth_by_code()

    def auth_by_code(self):
        auth_code = input("Copy the \"code\" query parameter and enter it here: ")
        code_verifier = self.random

        form_values = {
            "grant_type": "authorization_code",
            "client_id": self.settings['client_id'],
            "code": auth_code,
            "code_verifier": code_verifier
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com",
        }

        res = req.post(
            "https://login.eveonline.com/v2/oauth/token",
            data=form_values,
            headers=headers,
        )
        print(f'Code auth status - {res.status_code}')
        print('_________________________________________')
        auth_logger.info(f'Auth status code - {res.status_code}')
        auth_res = res.json()
        self.access_token = auth_res["access_token"]
        self.refresh_token = auth_res["refresh_token"]
        self.expired = int(auth_res["expires_in"]) + int(time.time())
        self.validate_auth()
        return self.create_label()

    def jwt_validate(self):
        jwt_base_url = 'https://login.eveonline.com/oauth/jwks'
        res = self.session.get(jwt_base_url)
        res.raise_for_status()

        data = res.json()

        jwk_sets = data["keys"]
        jwk_set = next((item for item in jwk_sets if item["alg"] == "RS256"))

        try:
            return jwt.decode(
                self.access_token,
                jwk_set,
                algorithms=jwk_set["alg"],
                issuer=self.login_jwt_url,
                options={"verify_aud": False}
            )
        except ExpiredSignatureError:
            print("The JWT token has expired: {}")
            auth_logger.error('The JWT token has expired')
            return None

    def validate_auth(self):
        validated_jwt = self.jwt_validate()
        self.character_id = validated_jwt["sub"].split(":")[2]
        self.character_name = validated_jwt["name"]

    def user_auth_object(self):
        self.user_auth = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expired": self.expired,
            "character_id": self.character_id,
            "character_name": self.character_name,
            "client_id": self.settings['client_id'],
            "scope": self.settings['scopes'],
            "resended_label_id": self.resended_label_id
        }
        # print(self.user_auth)
        return self.user_info_write()

    def user_info_write(self):
        directory = './user_data/'
        files = os.listdir(directory)
        try:
            with open(f'user_data/{self.character_name}_token_info.json', 'w') as users_list:
                json.dump(self.user_auth, users_list, indent=2)
                auth_logger.info(f"{self.character_name} user data file is created")
                print(f"{self.character_name} user data file is created")
                print('_________________________________________')
            # try:
                # refresh_token_dict = {
                #     "access_token": self.user_auth["access_token"],
                #     "expires_in": 1,
                #     "token_type": "Bearer",
                #     "refresh_token": self.user_auth["refresh_token"]
                # }
                # with open(f'user_data/{self.character_name}_refresh_token_info.json', 'w') as f:
                #     json.dump(refresh_token_dict, f, indent=2)
                #     print("Refresh token data file is created")
                #     print('_________________________________________')
                if 'users_list.json' in files:
                    with open(f'user_data/users_list.json', 'r') as file:
                        content = json.load(file)
                    with open(f'user_data/users_list.json', 'w') as ff:
                        content[self.character_name] = self.character_name
                        json.dump(content, ff, indent=2)
                        auth_logger.info("USERS LIST file is updated")
                        auth_logger.info('_________________________________________')
                        print("USERS LIST file is updated")
                        print('_________________________________________')
                else:
                    with open(f'user_data/users_list.json', 'w') as file:
                        users_list_dict = {self.character_name: self.character_name}
                        json.dump(users_list_dict, file, indent=2)
                        auth_logger.info("USERS LIST file is created")
                        auth_logger.info('_________________________________________')
                        print("USERS LIST file is created")
                        print('_________________________________________')
            # except:
            #     print('Some problem with creating refresh token data file')
            #     return None
        except:
            print('Some problem with creating user data file')
            auth_logger.error('Some problem with creating user data file')
            return None

    def create_label(self):
        get_labels = req.get(
            f'https://esi.evetech.net/latest/characters/{self.character_id}/mail/labels/?datasource=tranquility&token={self.access_token}')
        labels_list = get_labels.json()
        label_not_exists = True

        for el in labels_list["labels"]:
            if 'Resended' in el["name"]:
                label_not_exists = False
                self.resended_label_id = el["label_id"]
                print(f'Label already exists! Label ID - {el["label_id"]}')
                auth_logger.info(f'Label already exists! Label ID - {el["label_id"]}')
                break

        if label_not_exists:
            resend_label = {
                "color": "#00ff33",
                "name": "Resended",
            }
            create_resend_label = req.post(
                f'https://esi.evetech.net/latest/characters/{self.character_id}/mail/labels/?datasource=tranquility&token={self.access_token}',
                json=resend_label
            )
            if create_resend_label.status_code == 201:
                self.resended_label_id = create_resend_label.text
                print(f'Label successfully created! Label ID - {create_resend_label.text}')
                auth_logger.info(f'Label successfully created! Label ID - {create_resend_label.text}')
            else:
                print(f'{create_resend_label.status_code} - Label creating error')
                auth_logger.error(f'{create_resend_label.status_code} - Label creating error')
        print('_________________________________________')
        return self.user_auth_object()
