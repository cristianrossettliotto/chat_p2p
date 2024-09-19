import main

def request_message_validation(message):
    for address in main.list_of_addresses:
        print(f'Sending Message {message} to Validation to {address}')
        sockets.validation_socket.sendto(message, (sockets.broadcast_address, sockets.validtion_port))


def validation_daemon(stop_event, actual_number_of_nodes, message_queue):
       while not stop_event.is_set():
        try:
            data, addr = sockets.validation_socket.recvfrom(1024)
            if(data.decode('utf-8') == 'valid'):
                print('Mensage validada')
            else:
                print('Mensage invalidada')
        except BlockingIOError:
            continue
        except ValueError:
            continue