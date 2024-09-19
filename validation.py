import sockets

def request_message_validation(list_of_addresses, messages_to_validate):
    for message in messages_to_validate:
        for address in list_of_addresses:
            print(f'Sending Message {message} to Validation to {address}')
            sockets.validation_socket.sendto(message.encode('utf-8'), (address, sockets.validtion_port))


def validate_other_node_messages(stop_event, validated_messages, messages_to_validate):
       while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            message = data.decode('utf-8')
            if message in validated_messages or message in messages_to_validate:
                sockets.validation_socket.sendto('valid'.encode('utf-8'), (addr[0], sockets.validtion_port))
            else:
                sockets.validation_socket.sendto('invalid'.encode('utf-8'), (addr[0], sockets.validtion_port))
        except BlockingIOError:
            continue
        except ValueError:
            continue