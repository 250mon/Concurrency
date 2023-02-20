import asyncio
import socket
from asyncio import AbstractEventLoop
import logging


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # This will resolve the immediate issue of an exception causing our server to complain
    # that a task exception was never retrieved because we handle it in the coroutine itself.
    # It will also properly shut down the socket within the 'finally' block.

    # It's also import to note that this will properly close any connections
    # to clients we have open on application shutdown.
    # Because 'asyncio.run' will cancel any tasks we have remaining when our application
    # shuts down.
    # The important thing here is noting WHERE that exception is raised.
    # If our task is waiting on a statement such as 'await loop.sock_recv', and we cancel that task,
    # a 'Cancelled-Error' is thrown from the 'await loop.sock_recv' line.
    # This means that in the above case our 'finally' block will be executed,
    # since we threw an exception on an 'await' expression when we canceled the task.
    # If we change the exception block to catch and log these exceptions,
    # you will see one 'CancelledError' per each task that was created.
    try:
        while data := await loop.sock_recv(connection, 1024):
            print(data)
            if data == b'\r\n':
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())
