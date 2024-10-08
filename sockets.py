import socket

broadcast_ip = '0.0.0.0'
communication_port = 32000
notification_port = 32010
validtion_port = 32020
validtion_response_port = 32030
notification_exit_port = 32040
broadcast_address = '192.168.7.255'

def create_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((broadcast_ip, port))
    #sock.setblocking(False)
    return sock

notification_socket = create_socket(notification_port)
communication_socket = create_socket(communication_port)
validation_socket = create_socket(validtion_port)
validation_response_socket = create_socket(validtion_response_port)
notification_exit_socket = create_socket(notification_exit_port)

def close_sockets():
    communication_socket.close()
    notification_socket.close()
    validation_socket.close()
    validation_response_socket.close()
    notification_exit_socket.close()