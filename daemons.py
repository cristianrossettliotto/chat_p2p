from validation import request_message_validation
from time import sleep


def verify_messages_to_validate_queue(stop_event, list_of_addresses, messages_to_validate):
    old_messages_to_validate = []
    while not stop_event.is_set():
        if old_messages_to_validate != messages_to_validate:
            request_message_validation(list_of_addresses, messages_to_validate)
            old_messages_to_validate = messages_to_validate
        else:
            print(f'Function That Verify Messages to Validate: {messages_to_validate}\t{old_messages_to_validate}')