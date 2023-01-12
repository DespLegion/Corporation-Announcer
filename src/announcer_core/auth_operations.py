import json
import os
import logging as log

auth_op_logger = log.getLogger(__name__)
auth_op_logger.setLevel(log.INFO)
log_file_handler = log.FileHandler('./logs/auth_logs.log')
log_format = log.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
log_file_handler.setFormatter(log_format)
auth_op_logger.addHandler(log_file_handler)


class AuthOperations:
    def __init__(self):
        self.directory = './user_data/'
        self.files = os.listdir(self.directory)

    def get_chars_list(self, by_command_line=None):
        if 'users_list.json' in self.files:
            with open(f'user_data/users_list.json', 'r') as f:
                content = json.load(f)
                if by_command_line:
                    for user in content:
                        print(user)
            return content
        else:
            print('Users list do not created yet!')
            return None

    def delete_char(self, char_name):
        file_name = ''.join([char_name, '_token_info.json'])
        if file_name in self.files:
            os.remove(f'{self.directory}{file_name}')
            with open(f'user_data/users_list.json', 'r') as file:
                content = json.load(file)
            with open(f'user_data/users_list.json', 'w') as ff:
                content.pop(char_name)
                json.dump(content, ff, indent=2)
                print("USERS LIST file is updated")
            print(f'Character - {char_name} deleted')
            auth_op_logger.info(f"Character - {char_name} authorization deleted")
        else:
            print(f'No character with name - {char_name}')

    def delete_all(self):
        agreed = input('Are you sure you want to remove the authorization of all characters? Type "Yes" or "No": ')
        if agreed == 'Yes':
            char_list = self.get_chars_list()
            if not char_list:
                print('There are no authorized characters')
                return None
            for char in char_list:
                file_name = ''.join([char, '_token_info.json'])
                os.remove(f'{self.directory}{file_name}')
            os.remove(f'{self.directory}users_list.json')
            auth_op_logger.info(f"All authorizations deleted")
            print('All character authorizations deleted')
        else:
            print('Authorization deletion canceled')

    def get_char_info_for_resend(self, char_name):
        with open(f'{self.directory}{char_name}_token_info.json', 'r') as file:
            content = json.load(file)
        resend_info = {
            "access_token": content["access_token"],
            "character_id": content["character_id"],
            "resended_label_id": content["resended_label_id"]
        }
        return resend_info
