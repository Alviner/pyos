from socket import socket, AF_INET, SOCK_STREAM

from pyos5 import NewTask, Scheduler


def handle_client(client, addr):
    print(f"Connection from {addr}")
    while data := client.recv(65536):
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
        client, addr = sock.accept()

        yield NewTask(handle_client(cliend, addr))


def alive():
    while True:
        print("I'm alive")
        yield


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(alive())
    sched.new(server(45000))
    sched.mainloop()
