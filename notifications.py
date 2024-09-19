import sockets

def notify_other_nodes(notification_socket, local_ip):
    notification_socket.sendto(local_ip.encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))


def listen_notifications(notification_socket, stop_event, list_of_addresses):
   while not stop_event.is_set():
        try:
            data, addr = notification_socket.recvfrom(1024)
            if addr[0] != local_ip and addr[0] not in list_of_addresses:
                print(f'Adding Address {addr[0]} to list')
                list_of_addresses.append(addr[0])
                notification_socket.sendto(str(list_of_addresses).encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))
                print(f'List Addresses: {list_of_addresses}')
        except BlockingIOError:
            continue
        except ValueError:
            continue