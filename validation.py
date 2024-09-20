import sockets
from datetime import datetime
import time

def request_message_validation(list_of_addresses, messages_to_validate):
    time.sleep(1)
    for message_ip in messages_to_validate:
        message_received = message_ip[0]
        ip_from_sender = message_ip[1]
        for address in list_of_addresses:
            if ip_from_sender != address:
                print(f'Sending Message {message_received} to Validation to {address}')
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") + f".{current_time.microsecond // 1000:03d}"
                print(f'Send the request to validate The message with time {formatted_time}')
                sockets.validation_socket.sendto(message_received.encode('utf-8'), (address, sockets.validtion_port))


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate):
       while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f'Message Received: {message}')
            if message in validated_messages or message in messages_to_validate:
                print('Validated')
                sockets.validation_response_socket.sendto('valid'.encode('utf-8'), (addr[0], sockets.validtion_response_port))
            else:
                print('Invalidated')
                sockets.validation_response_socket.sendto('invalid'.encode('utf-8'), (addr[0], sockets.validtion_response_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue


def list_to_validation_response(stop_event):
       while not stop_event.is_set():
        try:
            data, addr = sockets.validation_response_socket.recvfrom(1024)
            message = data.decode('utf-8')
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") + f".{current_time.microsecond // 1000:03d}"
            print(f'Received the response to the request for validate The message with time {formatted_time}')
            print(f'Message From Validation: {message}')
        except BlockingIOError:
            continue
        except ValueError:
            continue
