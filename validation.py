import sockets
import json
from time import sleep

def request_message_validation(list_of_addresses, messages_to_validate):
    sleep(1)
    for message in messages_to_validate:
        message_to_send = message
        ip_from_sender = message['origin']
        for address in list_of_addresses:
            # if ip_from_sender != address:
            print(f'Method request_message_validation is calling for validation with IP {address} and Message {message_to_send}')
            sockets.validation_socket.sendto(json.dumps(message_to_send, indent=4, sort_keys=True, default=str  ).encode('utf-8'), (address, sockets.validtion_port))


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate):
    flag = False
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message_received_to_validate = json.loads(data.decode('utf-8'))

            print(f'Method validate_other_node_messages is validating message {message_received_to_validate}')

            for message in messages_to_validate:
                if message['content'] == message_received_to_validate['content']:
                    flag = True

            for message in validated_messages:
                if message['content'] == message_received_to_validate['content']:
                    flag = True

            if flag:
                print('valid')
                sockets.validation_response_socket.sendto('valid'.encode('utf-8'), (addr[0], sockets.validtion_response_port))
            else:
                print('invalid')
                sockets.validation_response_socket.sendto('invalid'.encode('utf-8'), (addr[0], sockets.validtion_response_port))
        
        except BlockingIOError:
            continue
        except ValueError:
            continue
    print('Method validate_other_node_messages is not responding anymore')


def list_to_validation_response(stop_event):
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_response_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f'Method list_to_validation_response received response from validation {message}')
        except BlockingIOError:
            continue
        except ValueError:
            continue
    print('Method list_to_validation_response is not responding anymore')
