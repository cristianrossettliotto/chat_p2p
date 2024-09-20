import sockets
from datetime import datetime

def receive_packtes(communication_socket, stop_event, local_ip, messages_to_validate):
    while not stop_event.is_set():
        try:
            data, addr = communication_socket.recvfrom(1024)
            message = data.decode('utf-8')

            if addr[0] != local_ip and not addr[0].startswith('127.'):
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") + f".{current_time.microsecond // 1000:03d}"
                print(f"Received message from {addr[0]}: {message}  with time {formatted_time}")
                messages_to_validate.append((message, addr[0]))
        except BlockingIOError:
            continue
        except ValueError:
            continue


def send_packets(communication_socket, stop_event):
    userInput = ''
    while True:
        userInput = input()
        if userInput.lower() in ("exit", "quit"):
            stop_event.set()
            sockets.close_sockets()
            break

        communication_socket.sendto(userInput.encode("utf-8"), (sockets.broadcast_address, sockets.communication_port))
