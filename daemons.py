from validation import request_message_validation
from datetime import datetime

def verify_messages_to_validate_queue(stop_event, list_of_addresses, messages_to_validate):
    old_messages_to_validate = []
    while not stop_event.is_set():
        if old_messages_to_validate != messages_to_validate:
            print('The Message Queue to validate has changed')
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") + f".{current_time.microsecond // 1000:03d}"
            print(f'Calling The Method to validate The message with time {formatted_time}')
            request_message_validation(list_of_addresses, messages_to_validate)
            old_messages_to_validate = messages_to_validate
            print(f'My new list: {old_messages_to_validate}')


