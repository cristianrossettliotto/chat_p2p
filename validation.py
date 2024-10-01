import sockets
import flet
import json
from time import sleep
from datetime import datetime

def request_message_validation(list_of_addresses, messages_to_validate):
    sleep(1)
    messages_to_remove = []

    for message in messages_to_validate:    
        print(f'Message On Request Validation: {message}')
        if message['already_validated']:
            continue

        if message['expiration_time'] <= datetime.now():
            messages_to_remove.append(message)
            continue

        for address in list_of_addresses:
            # if message['origin'] == address:
            #     continue
            
            message['already_validated'] = True
            sockets.validation_socket.sendto(json.dumps(message, indent=4, sort_keys=True, default=str  ).encode('utf-8'), (address, sockets.validtion_port))

    messages_to_validate = [msg for msg in messages_to_validate if msg not in messages_to_remove]


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate):
    flag = False
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message_received_to_validate = json.loads(data.decode('utf-8'))

            flag = any(
                message['content'] == message_received_to_validate['content']
                for message in messages_to_validate + validated_messages
            )

            print(f'Returning The Response Of Validation: {message_received_to_validate['id']}  {flag}')

            sockets.validation_response_socket.sendto(json.dumps({'id': message_received_to_validate['id'], 'result': flag}).encode('utf-8'), (addr[0], sockets.validtion_response_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue
    print('validate_other_node_messages Quiting')


def listen_to_validation_response(stop_event, messages_to_validate, list_of_addresses, validated_messages):
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_response_socket.recvfrom(1024)
            response = json.loads(data.decode('utf-8'))
            messages_to_remove = []

            for message in messages_to_validate:
                if message['id'] == response['id']:
                    print(f'Receiving Response From Validation Request: {message}')
                    message['validation_count'] = (message['validation_count'] + 1) if response['result'] else (message['validation_count'] - 1)

                    if (len(list_of_addresses) / 2) >= message['validation_count']:
                        validated_messages.append(message)
                        print(f'Validated Messages: {validated_messages}')
                        messages_to_remove.append(message)

            messages_to_validate = [message for message in messages_to_validate if message not in messages_to_remove]

        except BlockingIOError:
            continue
        except ValueError:
            continue
    print('listen_to_validation_response Quiting')
