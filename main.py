from threading import Thread, Event

import sockets
from local_ip import get_local_ip
from notifications import notify_other_nodes, listen_notifications
from communication import receive_packtes, send_packets
from daemons import verify_messages_to_validate_queue
from validation import validate_other_node_messages, list_to_validation_response

stop_event = Event()
list_of_addresses = []
messages_to_validate = []
validated_messages = []

local_ip = get_local_ip()

listen_packet_thread = Thread(
                            target=receive_packtes, 
                            args=(sockets.communication_socket, stop_event, local_ip, messages_to_validate))

send_packet_thread = Thread(
                            target=send_packets, 
                            args=(sockets.communication_socket, stop_event))

notification_thread = Thread(
                            target=listen_notifications,  
                            args=(sockets.notification_socket, stop_event, list_of_addresses, local_ip))

messages_to_validate_daemon = Thread(
                            target=verify_messages_to_validate_queue, 
                            args=(stop_event, list_of_addresses, messages_to_validate))


validate_other_messages_daemon = Thread(
                            target=validate_other_node_messages,
                            args=(stop_event, validated_messages, messages_to_validate))

list_to_validation_response_daemon = Thread(
                            target=list_to_validation_response,
                            args=(stop_event,))

notify_other_nodes(sockets.notification_socket, local_ip)

notification_thread.start()
listen_packet_thread.start()
send_packet_thread.start()
messages_to_validate_daemon.start()
validate_other_messages_daemon.start()
list_to_validation_response_daemon.start()

notification_thread.join()
listen_packet_thread.join()
send_packet_thread.join()
messages_to_validate_daemon.join()
validate_other_messages_daemon.join()
list_to_validation_response_daemon.join()