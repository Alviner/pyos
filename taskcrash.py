"""Python Operating System."""
from queue import Queue


class Task:
    """An object that runs operating system."""

    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


class Scheduler:
    """OS scheduler for task seitching."""

    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            result = task.run()
            self.schedule(task)


def foo():
    for _ in range(10):
        print("I'm foo")
        yield


def bar():
    while True:
        print("I'm bar")
        yield


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
