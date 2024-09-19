import sockets

def request_message_validation(validation_socket, message, list_of_addresses):
    for address in list_of_addresses:
        validation_socket.sendto(message, (sockets.broadcast_address, sockets.validtion_port))


def validation_daemon(validation_socket, stop_event, actual_number_of_nodes, message_queue):
       while not stop_event.is_set():
        try:
            data, addr = validation_socket.recvfrom(1024)
            if(data.decode('utf-8') == 'valid'):
                print('Mensage validada')
            else:
                print('Mensage invalidada')
        except BlockingIOError:
            continue
        except ValueError:
            continue