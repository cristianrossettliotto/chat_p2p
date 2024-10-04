import flet as ft
import uuid
from time import sleep
from flet import TextAlign
from threading import Event, Thread, Lock

from ips import get_local_ip, listen_nodes_exit
from notifications import notify_other_nodes, listen_notifications
from communication import receive_packets, send_packets
from validation import validate_other_node_messages, listen_to_validation_response

stop_event = Event()
list_of_addresses = []
messages_to_validate = []
validated_messages = []
global_mutex = Lock()

local_ip = get_local_ip()

def create_interface(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Chat Peer To Peer"

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    list = ft.ListView(
        expand=True,
        spacing=5,
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
        disabled= True,
        on_submit=lambda e: handle_send_message()
    )

    def show_adresses():
        local_addresses = []
        text_controls = {}  # Dicionário para armazenar referências a ft.Text por endereço

        while not stop_event.is_set():
            with global_mutex:
                for address in list_of_addresses:
                    if address not in local_addresses:
                        local_addresses.append(address)
                        text_control = ft.Text(address)  # Cria o controle de texto
                        text_controls[address] = text_control  # Armazena a referência do ft.Text
                        list.controls.append(text_control)
                        new_message.disabled = len(local_addresses) < 1
                        page.update()

                addresses_to_remove = []

                for address in local_addresses:
                    if address not in list_of_addresses:
                        addresses_to_remove.append(address)

                for address in addresses_to_remove:
                    local_addresses.remove(address)
                    if address in text_controls:
                        list.controls.remove(text_controls[address])  # Usa a referência existente
                        del text_controls[address]  # Remove a referência do dicionário
                    page.update()


    def show_validated_message():
        while not stop_event.is_set():
            with global_mutex:
                for message in validated_messages:
                        
                    if message['already_showed']:
                        continue

                    message['already_showed'] = True
                    chat.controls.append(ft.Text(f"{message['content']}"))
                    page.update()
            sleep(0.5)


    def handle_send_message():
        if new_message.value == '' or stop_event.is_set():
            return
        message = {'id': uuid.uuid4(), 'already_validated': False, 'already_showed': False, 'content': new_message.value, 'origin': local_ip, 'author': '', 'validation_count': 0, 'expiration_time': ''}
        send_packets(stop_event, local_ip, message, page)
        new_message.value = ""
        new_message.focus()

    threads = [
        Thread(target = show_validated_message), 
        Thread(target=show_adresses)
    ]
    
    for thread in threads:
        thread.start()

    page.add(
        
        ft.Row(
            [
                ft.Text("To Exit Enter: exit, quit, q or x", size=15, text_align=TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.Container(
                    content=chat,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),

                ft.Container(
                    content=list,
                    width=200,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=5,
                ),
            ],
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
    Thread(target=receive_packets, args=(stop_event, local_ip, messages_to_validate, list_of_addresses, global_mutex)),
    Thread(target=listen_notifications, args=(stop_event, list_of_addresses, local_ip, global_mutex)),
    Thread(target=validate_other_node_messages, args=(stop_event, validated_messages, messages_to_validate, global_mutex)),
    Thread(target=listen_to_validation_response, args=(stop_event, messages_to_validate, list_of_addresses, validated_messages, global_mutex)),
    Thread(target=listen_nodes_exit, args=(stop_event, list_of_addresses, global_mutex))
]


for thread in threads:
    thread.start()

notify_other_nodes(local_ip)

ft.app(target=create_interface)

for thread in threads:
    thread.join()