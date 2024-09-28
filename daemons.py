from validation import request_message_validation
from time import sleep


def verify_messages_to_validate_queue(list_of_addresses, messages_to_validate):
    print(f'DAEMON: UPDATING LOCAL QUEUE WITH {messages_to_validate}')
    request_message_validation(list_of_addresses, messages_to_validate)
    old_messages_to_validate = messages_to_validate