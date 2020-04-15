from socket import socket, AF_INET, SOCK_STREAM

from pyos8 import NewTask, Scheduler, Recv, Send, Accept


def handle_client(client, addr):
    print(f"Connection from {addr}")
    while True:
        data = yield Recv(client, 65536)
        if not data:
            break
        yield Send(client, data)
    client.close()
    print("Client closed")


def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        client, addr = yield Accept(sock)
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
