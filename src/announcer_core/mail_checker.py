import requests as req
import logging as log


mail_logger = log.getLogger(__name__)
mail_logger.setLevel(log.INFO)
log_file_handler = log.FileHandler('./logs/mail_resender_logs.log')
log_format = log.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
log_file_handler.setFormatter(log_format)
mail_logger.addHandler(log_file_handler)


class MailResender:

    def __init__(self, white_list, npc_corp_list, char_data_dict, char_name, source='tranquility'):
        self.token = char_data_dict["access_token"]
        self.white_list = white_list
        self.npc_corp_list = npc_corp_list
        self.char_id = char_data_dict["character_id"]
        self.label_id = char_data_dict["resended_label_id"]
        self.recipient_corp_id = 1
        self.source = source
        self.base_url = 'https://esi.evetech.net/latest/characters/'
        self.char_name = char_name

    def get_mails_headers(self):
        mail_logger.info(f'Resender for {self.char_name} started')
        data = req.get(
            f'{self.base_url}{self.char_id}/mail/?datasource={self.source}&token={self.token}')
        if data.status_code == 200:
            dict_data = data.json()
            return self.get_needed_mail(dict_data)
        else:
            mail_logger.error(f'Error {data.status_code} with mail list update')
            return None

    def send_try(self, mail):
        send = req.post(
            f'{self.base_url}{self.char_id}/mail/?character_id={self.recipient_corp_id}&datasource={self.source}&token={self.token}',
            json=mail)
        if send.status_code == 201:
            return send
        else:
            mail_logger.error(f'{self.char_name} - {send.text} Error with sending message {send.status_code}')

    def form_mail(self, data):
        mail = {
            'approved_cost': 0,
            'body': data['body'],
            'recipients': [
                {
                    'recipient_id': self.recipient_corp_id,
                    'recipient_type': 'corporation'
                }
            ],
            'subject': data['subject']
        }
        return mail

    def get_corp_recipient_id(self):
        data = req.get(
            f'{self.base_url}{self.char_id}/?datasource={self.source}')
        if data.status_code == 200:
            self.recipient_corp_id = data.json()["corporation_id"]
            return self.recipient_corp_id
        else:
            mail_logger.error(f'Error with corporation ID update')
            return None

    def get_needed_mail(self, dict_data):
        needed_mail = []
        corp_id = self.get_corp_recipient_id()
        if corp_id in self.npc_corp_list:
            mail_logger.error(f'{self.char_name} in NPC corporation')
            return None

        for mail in dict_data:
            if mail["from"] in self.white_list and "is_read" not in mail:
                needed_mail.append(mail["mail_id"])

        if any(needed_mail):
            for mail_id in needed_mail:
                data = req.get(
                    f'{self.base_url}{self.char_id}/mail/{mail_id}/?datasource={self.source}&token={self.token}'
                )
                if data.status_code == 200:
                    mail_to_resend = self.form_mail(data.json())
                    status = self.send_try(mail_to_resend)
                    if status.status_code == 201:
                        mail_logger.info(f'{self.char_name} - mail {mail_id} resended')
                        updated_info = {
                            "labels": [
                                1,
                                self.label_id,
                            ],
                            "read": True
                        }
                        data2 = req.put(
                            f'{self.base_url}{self.char_id}/mail/{mail_id}/?datasource={self.source}&token={self.token}',
                            json=updated_info
                        )
                        # if data2.status_code == 204:
                        #     mail_logger.info(f'{self.char_name} - {mail_id} Mail info updated')
                        # else:
                        #     mail_logger.error(f'{self.char_name} - {data2.status_code} Error with update mail info')

                        if data2.status_code != 204:
                            mail_logger.error(f'{self.char_name} - {data2.status_code} Error with update mail info')
                else:
                    mail_logger.error(f'Error {data.status_code} with getting mail - {mail_id}')
        else:
            mail_logger.info(f'No mails for resend')
        return needed_mail
