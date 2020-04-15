from socket import socket, AF_INET, SOCK_STREAM

from pyos8 import NewTask, Scheduler, Recv, Send, Accept
from sockwrap import Socket


def handle_client(client, addr):
    print(f"Connection from {addr}")
    while True:
        data = yield client.recv(65536)
        if not data:
            break
        yield client.send( data)
    client.close()
    print("Client closed")


def server(port):
    print("Server starting")
    raw_sock = socket(AF_INET, SOCK_STREAM)
    raw_sock.bind(("", port))
    raw_sock.listen(5)
    sock = Socket(raw_sock)
    while True:
        client, addr = yield sock.accept()
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
