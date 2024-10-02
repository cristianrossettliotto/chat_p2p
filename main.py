import flet as ft
import uuid
from time import sleep
from flet import TextAlign
from threading import Event, Thread

import sockets
from local_ip import get_local_ip
from notifications import notify_other_nodes, listen_notifications
from communication import receive_packets, send_packets
from validation import validate_other_node_messages, listen_to_validation_response

stop_event = Event()
list_of_addresses = []
messages_to_validate = []
validated_messages = []

local_ip = get_local_ip()

def create_interface(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Chat Peer To Peer"

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=lambda e: handle_send_message()
    )

    def show_validated_message():
        print('ENTROU NA FUNCAO QUE VALIDA ESSA PORRA')
        while not stop_event.is_set():
            for message in validated_messages:
                print(f'Caiu AQUIII {message['already_showed']}')
                if message['already_showed']:
                    continue
                print('Caiu AQUIII')
                message['already_showed'] = True
                chat.controls.append(ft.Text(f"{['content']}"))
                page.update()
            sleep(0.5)


    def handle_send_message():
        if new_message.value == '' or stop_event.is_set():
            return
        message = {'id': uuid.uuid4(), 'already_validated': False, 'already_showed': False, 'content': new_message.value, 'origin': local_ip, 'author': '', 'validation_count': 0, 'expiration_time': ''}
        send_packets(sockets.communication_socket, stop_event, local_ip, message, page)
        new_message.value = ""
        new_message.focus()

    thread = Thread(target = show_validated_message)
    thread.start()

    page.add(
        
        ft.Row(
            [
                ft.Text("To Exit Enter: exit, quit, q or x", size=15, text_align=TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),

        ft.Row(
            [        
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=lambda e: handle_send_message()
                ),
            ]
        ),
    )




threads = [
    Thread(target=receive_packets, args=(sockets.communication_socket, stop_event, local_ip, messages_to_validate, list_of_addresses)),
    Thread(target=listen_notifications, args=(sockets.notification_socket, stop_event, list_of_addresses, local_ip)),
    Thread(target=validate_other_node_messages, args=(stop_event, validated_messages, messages_to_validate)),
    Thread(target=listen_to_validation_response, args=(stop_event, messages_to_validate, list_of_addresses, validated_messages))
]

notify_other_nodes(sockets.notification_socket, local_ip)

for thread in threads:
    thread.start()

ft.app(target=create_interface)

for thread in threads:
    thread.join()