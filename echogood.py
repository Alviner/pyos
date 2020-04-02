from socket import socket, AF_INET, SOCK_STREAM

from pyos7 import NewTask, Scheduler, ReadWait, WriteWait


def handle_client(client, addr):
    print(f"Connection from {addr}")
    while True:
        yield ReadWait(client)
        data = client.recv(65536)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)
    client.close()
    print("Client closed")
    yield  # make it a coro


def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        yield ReadWait(sock)
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))


def alive():
    while True:
        print("I'm alive")
        yield


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(alive())
    sched.new(server(45000))
    sched.mainloop()
