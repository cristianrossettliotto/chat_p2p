import sockets
import json
from time import sleep
from datetime import datetime, timedelta

def receive_packtes(communication_socket, stop_event, local_ip, messages_to_validate):
    while not stop_event.is_set():
        try:
            data, addr = communication_socket.recvfrom(1024)
            message =  json.loads(data.decode('utf-8'))
            current_time = datetime.now()
            expiration_time = current_time + timedelta(seconds=15)
            message['expiration_time'] = expiration_time

            if addr[0] != local_ip and not addr[0].startswith('127.'):
                messages_to_validate.append(message)
            else:
                sleep(1)
                messages_to_validate.append(message)

        except BlockingIOError:
            continue
        except ValueError:
            continue


def send_packets(communication_socket, stop_event, local_ip):
    userInput = ''
    while True:
        userInput = input()
        if userInput.lower() in ("exit", "quit", "x", "q"):
            stop_event.set()
            sockets.close_sockets()
            break

        communication_socket.sendto(
            json.dumps({'content': userInput, 'origin': local_ip, 'author': '','validation_count': 0, 'expiration_time': ''}, indent=4, sort_keys=True, default=str).encode('utf-8'), 
            (sockets.broadcast_address, sockets.communication_port))