import sockets
import json

def notify_other_nodes(local_ip):

    sockets.notification_socket.sendto(
        json.dumps(local_ip, indent=4, sort_keys=True, default=str).encode('utf-8'), 
        (sockets.broadcast_address, sockets.notification_port))


def listen_notifications(stop_event, list_of_addresses, local_ip):
    while not stop_event.is_set():
        try:
            data, addr = sockets.notification_socket.recvfrom(1024)
            content =  json.loads(data.decode('utf-8'))

            if addr[0] != local_ip:
                list_of_addresses.append(addr[0])

            if type(content) == str and data not in list_of_addresses:
                list_of_addresses.append(addr[0])
                
            if type(content) == list:
                for address in content:
                    if address not in list_of_addresses:
                        list_of_addresses.append(address)

            print(f'Final Result: {list_of_addresses}')
            sockets.notification_socket.sendto(str(list_of_addresses).encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue
