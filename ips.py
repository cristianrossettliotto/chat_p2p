import socket
import sockets

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except Exception:
            return '127.0.0.1'


def notify_other_nodes_of_exit():
    sockets.notification_exit_socket.sendto(str(get_local_ip()).encode('utf-8'), 
    (sockets.broadcast_address, sockets.notification_exit_port))


def listen_nodes_exit(stop_event, list_of_addresses, global_mutex):
    while not stop_event.is_set():
        try:
            data, addr = sockets.notification_exit_socket.recvfrom(1024)
            message =  data.decode('utf-8')

            with global_mutex:
                print(f'Removing: {message}')
                list_of_addresses.remove(message)
                print(f'List Of Addresses: {list_of_addresses}')
        except BlockingIOError:
            continue
        except ValueError:
            continue
