from validation import request_message_validation
from time import sleep


def verify_messages_to_validate_queue(stop_event, list_of_addresses, messages_to_validate):
    old_messages_to_validate = []
    while not stop_event.is_set():
        if old_messages_to_validate != messages_to_validate:
            print(f'Method verify_messages_to_validate_queue is calling the method request_message_validation with queue {messamessages_to_validatege}')
            request_message_validation(list_of_addresses, messages_to_validate)
            old_messages_to_validate = messages_to_validate
        else:
            sleep(1)
    print('Method verify_messages_to_validate_queue is not responding anymore')