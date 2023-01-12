from settings import app_settings as settings
from settings import white_list, npc_corp_list
from src.announcer_core.auth import InitCharAuth
from src.announcer_core.mail_checker import MailResender
from src.announcer_core.token_operations import TokenOperations
from src.announcer_core.auth_operations import AuthOperations

init_auth = InitCharAuth(settings)
auth_operations = AuthOperations()


def execute_from_command_line(argv=None):
    if len(argv) == 1:
        char_list = auth_operations.get_chars_list()
        for char in char_list:
            token_update = TokenOperations(settings, char)
            token_update.token_update()
            char_data_dict = auth_operations.get_char_info_for_resend(char)
            resender = MailResender(white_list, npc_corp_list, char_data_dict, char)
            resender.get_mails_headers()
    elif argv[1] == 'auth':
        init_auth.print_auth_url()
        print('Authorization is Done')
    elif argv[1] == 'users_list':
        auth_operations.get_chars_list(by_command_line=True)
    elif argv[1] == 'force_update':
        if len(argv) > 2:
            char_name = argv[2]
            format_name = char_name.replace('_', ' ')
            token_update = TokenOperations(settings, format_name)
            token_update.token_update(by_command_line=True)
        else:
            print('You need to enter character name!')
    elif argv[1] == 'delete':
        if len(argv) > 2:
            if argv[2] == 'all':
                auth_operations.delete_all()
            else:
                char_name = argv[2]
                format_name = char_name.replace('_', ' ')
                auth_operations.delete_char(format_name)
        else:
            print('You need to enter character name!')
    else:
        print('Unknown command')
