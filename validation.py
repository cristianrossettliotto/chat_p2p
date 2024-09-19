import sockets

def request_message_validation(list_of_addresses, messages_to_validate):
    for message in messages_to_validate:
        for address in list_of_addresses:
            print(f'Sending Message {message} to Validation to {address}')
            sockets.validation_socket.sendto(message.encode('utf-8'), (sockets.broadcast_address, sockets.validtion_port))


def validate_other_node_messages(stop_event):
       while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
        except BlockingIOError:
            continue
        except ValueError:
            continue