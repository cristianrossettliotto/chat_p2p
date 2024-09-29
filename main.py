from threading import Thread, Event

import sockets
from local_ip import get_local_ip
from notifications import notify_other_nodes, listen_notifications
from communication import receive_packets, send_packets
from validation import validate_other_node_messages, list_to_validation_response

stop_event = Event()
list_of_addresses = []
messages_to_validate = []
validated_messages = []

local_ip = get_local_ip()

threads = [
    Thread(target=receive_packets, args=(sockets.communication_socket, stop_event, local_ip, messages_to_validate, list_of_addresses)),
    Thread(target=send_packets, args=(sockets.communication_socket, stop_event, local_ip)),
    Thread(target=listen_notifications, args=(sockets.notification_socket, stop_event, list_of_addresses, local_ip)),
    Thread(target=validate_other_node_messages, args=(stop_event, validated_messages, messages_to_validate)),
    Thread(target=list_to_validation_response, args=(stop_event, messages_to_validate, list_of_addresses, validated_messages))
]

notify_other_nodes(sockets.notification_socket, local_ip)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()