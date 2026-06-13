from task import Task

class Asset:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        if not isinstance(component, Component):
            raise TypeError("component must be a Component instance")
        self.components.append(component)

class Component():
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance")
        self.tasks.append(task)
