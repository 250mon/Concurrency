from threading import Thread
import socket


# The problem with the following thread, it doesn't accept
# a keyboard interrupt
# That's why we need either of daemonic thread or a thread
# which is able to handle interrupts

def echo(client: socket):
    while True:
        data = client.recv(2048)
        print(f'Received {data}, sending!')
        client.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind('127.0.0.1', 8000)
    server.listen()
    while True:
        connection, _ = server.accept()
        thread = Thread(target=echo, args=(connection,))
        # making it daemonic
        # thread.daemon = True
        thread.start()