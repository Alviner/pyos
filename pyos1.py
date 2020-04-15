"""Python Operating System."""


class Task:
    """An object that runs operating system."""

    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        return self.target.send(self.sendval)


if __name__ == "__main__":
    def foo():
        print("Part 1")
        yield
        print("Part 2")
        yield

    t1 = Task(foo())
    t1.run()
    t1.run()
