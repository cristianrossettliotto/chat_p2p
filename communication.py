import sockets
import json
import uuid
from time import sleep
from datetime import datetime, timedelta
from validation import request_message_validation

def receive_packets(communication_socket, stop_event, local_ip, messages_to_validate, list_of_addresses):
    while not stop_event.is_set():
        try:
            data, addr = communication_socket.recvfrom(1024)
            message =  json.loads(data.decode('utf-8'))
            current_time = datetime.now()
            expiration_time = current_time + timedelta(seconds=15)
            message['expiration_time'] = expiration_time
            messages_to_validate.append(message)

            if addr[0] == local_ip or addr[0].startswith('127.'):
                sleep(1)

            print(f'Message Received 2: {message}')   

            request_message_validation(list_of_addresses, messages_to_validate)
        except BlockingIOError:
            continue
        except ValueError:
            continue
    print('receive_packets Quiting')



def send_packets(communication_socket, stop_event, local_ip, message, page):
    if message.lower() in ("exit", "quit", "x", "q"):
        print('send_packets Quiting')
        stop_event.set()
        sockets.close_sockets()
        page.window_close()
        return
    
    print('Sending')
    communication_socket.sendto(
        json.dumps({'id': uuid.uuid4(), 'already_validated': False, 'content': message, 'origin': local_ip, 'author': '', 'validation_count': 0, 'expiration_time': ''}, indent=4, sort_keys=True, default=str).encode('utf-8'), 
        (sockets.broadcast_address, sockets.communication_port))

    message = ''