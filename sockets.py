import socket

broadcast_ip = '0.0.0.0'
communication_port = 5000
notification_port = 5010
validtion_port = 5020
validtion_response_port = 5030
broadcast_address = '192.168.7.255'

notification_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
notification_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
notification_socket.bind((broadcast_ip, notification_port))

communication_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
communication_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
communication_socket.bind((broadcast_ip, communication_port))

validation_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
validation_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
validation_socket.bind((broadcast_ip, validtion_port))

validation_response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
validation_response_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
validation_response_socket.bind((broadcast_ip, validtion_response_port))

communication_socket.setblocking(False)
notification_socket.setblocking(False)
validation_socket.setblocking(False)

def close_sockets():
    communication_socket.close()
    notification_socket.close()
    validation_socket.close()
    validation_response_socket.close()