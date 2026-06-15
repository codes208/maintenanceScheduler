from task import MeteringTask, Task

class Asset:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        if not isinstance(component, Component):
            raise TypeError("component must be a Component instance")
        self.components.append(component)

class Component():
    def __init__(self, name, has_meter=False, meter_reading=None):
        if not has_meter and meter_reading is not None:
            raise ValueError("a component without a meter cannot have a meter_reading")
        self.name = name
        self.has_meter = has_meter
        self.meter_reading = meter_reading
        self.tasks = []

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance")
        if isinstance(task, MeteringTask) and not self.has_meter:
            raise ValueError("cannot add a metering task to a component without a meter")
        self.tasks.append(task)

    def meter_update(self, new_reading):
        if not self.has_meter:
            raise ValueError(f"Component {self.name} has no meter")
        if new_reading < 0:
            raise ValueError(f"new_reading cannnot be negative (got {new_reading})")
        highest_service = max(
            (task.last_serviced for task in self.tasks if isinstance(task, MeteringTask)),
            default=0
        )
        if new_reading < highest_service:
            raise ValueError(f"reading ({new_reading}) cannot be below the latest serviced point ({highest_service})")
        self.meter_reading = new_reading
