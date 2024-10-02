import sockets

def notify_other_nodes(local_ip):
    sockets.notification_socket.sendto(local_ip.encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))


def listen_notifications(stop_event, list_of_addresses, local_ip):
    while not stop_event.is_set():
        try:
            data, addr = sockets.notification_socket.recvfrom(1024)
            if addr[0] != local_ip and addr[0] not in list_of_addresses:
                list_of_addresses.append(addr[0])
                sockets.notification_socket.sendto(str(list_of_addresses).encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue
