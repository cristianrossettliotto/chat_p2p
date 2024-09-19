from threading import Thread, Event

import sockets
from local_ip import get_local_ip
from notifications import notify_other_nodes, listen_notifications
from communication import receive_packtes, send_packets

stop_event = Event()
list_of_addresses = []

local_ip = get_local_ip()

listen_packet_thread = Thread(target=receive_packtes, args=(sockets.communication_socket, stop_event))
send_packet_thread = Thread(target=send_packets, args=(sockets.communication_socket, stop_event))
notification_thread = Thread(target=listen_notifications,  args=(sockets.notification_socket, stop_event, list_of_addresses))

notify_other_nodes(sockets.notification_socket, local_ip)

notification_thread.start()
listen_packet_thread.start()
send_packet_thread.start()

send_packet_thread.join()
listen_packet_thread.join()
notification_thread.join()

