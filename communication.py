import sockets
import json
from time import sleep
from datetime import datetime, timedelta
from validation import request_message_validation

def receive_packets(stop_event, local_ip, messages_to_validate, list_of_addresses, global_mutex):
    while not stop_event.is_set():
        try:
            data, addr = sockets.communication_socket.recvfrom(1024)
            message =  json.loads(data.decode('utf-8'))

            with global_mutex:    
                message['expiration_time'] = (datetime.now() + timedelta(seconds=15))
                messages_to_validate.append(message)

            if addr[0] == local_ip or addr[0].startswith('127.'):
                sleep(1)  

            request_message_validation(list_of_addresses, messages_to_validate, global_mutex)
        except BlockingIOError:
            continue
        except ValueError:
            continue



def send_packets(stop_event, local_ip, message, page):
    if message['content'].lower() in ("exit", "quit", "x", "q"):
        stop_event.set()
        sockets.close_sockets()
        page.window_close()
        return
    
    sockets.communication_socket.sendto(
        json.dumps(message, indent=4, sort_keys=True, default=str).encode('utf-8'), 
        (sockets.broadcast_address, sockets.communication_port))