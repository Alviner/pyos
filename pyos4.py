"""Python Operating System."""
from abc import ABC, abstractmethod
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


class SystemCall(ABC):
    @abstractmethod
    def handle(self):
        raise NotImplementedError


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


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

    def exit(self, task):
        print(f"Task {task.tid} terminated")
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


def foo():
    myid = yield GetTid()
    for _ in range(10):
        print(f"I'm foo {myid}")
        yield


def bar():
    myid = yield GetTid()
    for _ in range(5):
        print(f"I'm bar {myid}")
        yield


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
