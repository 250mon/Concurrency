import socket

# AF_INET : type of address; a hostnmae and a port number
# SOCK_STREM : tcp connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO_REUSEADDR : reuse the port number after we stop and restart
# the application, avoiding any address already in use errors
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
# mak the server socket as non-blocking
server_socket.setblocking(False)

connections = []

try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            # mark the client socket as non blocking
            connection.setblocking(False)
            print(f'I got a connection from {client_address}')
            connections.append(connection)
        except BlockingIOError:
            pass

        for connection in connections:
            try:
                buffer = b''

                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f'I got data:{data}!')
                        buffer = buffer + data

                print(f"All the data is: {buffer}")
                connection.send(buffer)
            except BlockingIOError:
                pass

finally:
    server_socket.close()
