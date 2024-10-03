import sockets
import json

def notify_other_nodes(local_ip):
    sockets.notification_socket.sendto(
        json.dumps(local_ip).encode('utf-8'), 
        (sockets.broadcast_address, sockets.notification_port))


def listen_notifications(stop_event, list_of_addresses, local_ip, global_mutex):
    changed = False
    print(f'Listen Notification Start: {list_of_addresses} {id(list_of_addresses)} ')
    while not stop_event.is_set():
        try:
            data, addr = sockets.notification_socket.recvfrom(1024)
            content = json.loads(data.decode('utf-8'))
            temp_list = []

            with global_mutex:
                if addr[0] != local_ip:
                    temp_list.append(addr[0])

                if type(content) == str and content not in temp_list and content != local_ip:
                    temp_list.append(content)
                    
                if type(content) == list:
                    for address in content:
                        if address not in temp_list and address != local_ip:
                            temp_list.append(address)

                for address in temp_list:
                    if address not in list_of_addresses:
                        changed = True
                        list_of_addresses.append(address)

                print(f'Listen Notification: {list_of_addresses} {id(list_of_addresses)} ')
                if changed:
                    changed = False
                    sockets.notification_socket.sendto(json.dumps(list_of_addresses).encode('utf-8'), (sockets.broadcast_address, sockets.notification_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue
