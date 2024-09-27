import sockets
from datetime import datetime, timedelta

def receive_packtes(communication_socket, stop_event, local_ip, messages_to_validate):
    while not stop_event.is_set():
        try:
            data, addr = communication_socket.recvfrom(1024)
            message = data.decode('utf-8')

            if addr[0] != local_ip and not addr[0].startswith('127.'):
                print(f'Message Received: {message}')
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

        current_time = datetime.now()
        expiration_time = current_time + timedelta(seconds=15)

        
        communication_socket.sendto(
            str({'content': userInput, 'origin': local_ip, 'author': '','validation_count': 0, 'expiration_time': null}).encode("utf-8"), 
            (sockets.broadcast_address, sockets.communication_port))