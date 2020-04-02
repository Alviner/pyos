"""Python Operating System."""
from abc import ABC, abstractmethod
from select import select
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


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        # If waiting for a non-existent task,
        # return emmidiately without waiting
        if not result:
            self.sched.schedule(self.task)


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task, fd)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fineno()
        self.sched.waitforwrite(self.task, fd)


class Scheduler:
    """OS scheduler for task seitching."""

    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.exit_waiting = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def waitforread(self, task, fd):
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):
        self.write_waiting[fd] = task

    def ipoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = (
                select(self.read_waiting, self.write_waiting, [], timeout)
            )
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))
            for fd in r:
                self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        while True:
            timeout = None if self.ready.empty() else 0
            self.ipoll(timeout)
            yield

    def exit(self, task):
        print(f"Task {task.tid} terminated")
        del self.taskmap[task.tid]
        # Notify other tasks waiting for exit
        for task in self.exit_waiting.pop(task.tid, {}):
            self.schedule(task)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        return False

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        self.new(self.iotask())
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
    for i in range(5):
        print(f"I'm foo {myid}")
        yield


def main():
    child = yield NewTask(foo())
    print("Waiting for child")
    yield WaitTask(child)
    print("Child done")


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
