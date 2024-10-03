import sockets
import flet
import json
from time import sleep
from datetime import datetime

def request_message_validation(list_of_addresses, messages_to_validate, global_mutex):
    sleep(1)
    messages_to_remove = []

    with global_mutex:
        for message in messages_to_validate:
            if message['already_validated']:
                continue
            
            data = datetime.now()
            if message['expiration_time'] <= data:
                messages_to_remove.append(message)
                continue

            for address in list_of_addresses:
                if message['origin'] == address:
                    continue
                
                message['already_validated'] = True
                sockets.validation_socket.sendto(json.dumps(message, indent=4, sort_keys=True, default=str  ).encode('utf-8'), (address, sockets.validtion_port))

        for message in messages_to_remove:
            if message in messages_to_validate:
                messages_to_validate.remove(message)


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate, global_mutex):
    flag = False
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message_received_to_validate = json.loads(data.decode('utf-8'))

            with global_mutex:
                flag = any(
                    message['content'] == message_received_to_validate['content']
                    for message in messages_to_validate + validated_messages
                )

            sockets.validation_response_socket.sendto(json.dumps({'id': message_received_to_validate['id'], 'result': flag}).encode('utf-8'), (addr[0], sockets.validtion_response_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue


def listen_to_validation_response(stop_event, messages_to_validate, list_of_addresses, validated_messages, global_mutex):
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_response_socket.recvfrom(1024)
            response = json.loads(data.decode('utf-8'))
            messages_to_remove = []

            with global_mutex:
                for message in messages_to_validate:
                    if message['id'] == response['id']:
                        message['validation_count'] = (message['validation_count'] + 1) if response['result'] else (message['validation_count'] - 1)

                        if message['validation_count']:
                            validated_messages.append(message)
                            messages_to_remove.append(message)

                for message in messages_to_remove:
                    if message in messages_to_validate:
                        messages_to_validate.remove(message)

        except BlockingIOError:
            continue
        except ValueError:
            continue
