import sockets
import json
from time import sleep

def request_message_validation(list_of_addresses, messages_to_validate):
    sleep(1)
    print(f'Validation Message: {messages_to_validate}')
    for message in messages_to_validate:
        if message['already_validated']:
            continue

        message_to_send = message
        ip_from_sender = message['origin']

        print(f'Ip Addresses: {list_of_addresses}')
        print(f'Will Validate Message {message_to_send}')
        for address in list_of_addresses:
            if ip_from_sender != address:
                message_to_send['already_validated'] = True
                sockets.validation_socket.sendto(json.dumps(message_to_send, indent=4, sort_keys=True, default=str  ).encode('utf-8'), (address, sockets.validtion_port))


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate):
    flag = False
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message_received_to_validate = json.loads(data.decode('utf-8'))

            for message in messages_to_validate:
                if message['content'] == message_received_to_validate['content']:
                    flag = True

            for message in validated_messages:
                if message['content'] == message_received_to_validate['content']:
                    flag = True

            if flag:
                sockets.validation_response_socket.sendto(json.dumps({'id': message_received_to_validate['id'], 'result': True}).encode('utf-8'), (addr[0], sockets.validtion_response_port))
            else:
                sockets.validation_response_socket.sendto(json.dumps({'id': message_received_to_validate['id'], 'result': False}).encode('utf-8'), (addr[0], sockets.validtion_response_port))
        
        except BlockingIOError:
            continue
        except ValueError:
            continue


def list_to_validation_response(stop_event, messages_to_validate, list_of_addresses, validated_messages):
    while not stop_event.is_set():
        try:
            data, addr = sockets.validation_response_socket.recvfrom(1024)
            response = json.loads(data.decode('utf-8'))
            
            for message in messages_to_validate:
                if message['id'] == response['id']:
                    message['validation_count'] = (message['validation_count'] + 1) if response['result'] else (message['validation_count'] - 1)

                    if (len(list_of_addresses) / 2) >= message['validation_count']:
                            validated_messages.append(message)
                            print(f'Validated Messages: {validated_messages}')
                            messages_to_validate.remove(message)
                            print(f'Message To Validate: {messages_to_validate}')

        except BlockingIOError:
            continue
        except ValueError:
            continue
