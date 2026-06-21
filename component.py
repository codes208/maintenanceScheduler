from task import MeteringTask, Task, STATUS_ORDER, task_from_dict

# Add a delete component function

class Component():
    def __init__(self, name, has_meter=False, meter_reading=None):
        if not has_meter and meter_reading is not None:
            raise ValueError("a component without a meter cannot have a meter_reading")
        self.name = name
        self.has_meter = has_meter
        self.meter_reading = meter_reading
        self.tasks = []

    def _task_status(self, task):
        if isinstance(task, MeteringTask) and self.meter_reading is None:
            return "unknown"
        return task.maintenance_due(self.meter_reading)

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance")
        if isinstance(task, MeteringTask) and not self.has_meter:
            raise ValueError("cannot add a metering task to a component without a meter")
        for existing in self.tasks:
            if existing.name == task.name:
                raise ValueError(f"a task named '{task.name}' already exists in this list of tasks")

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

    def status(self):
        if not self.tasks:
            return "ok"
        statuses = []
        for task in self.tasks:
            statuses.append(self._task_status(task))
        return max(statuses, key=lambda s: STATUS_ORDER.index(s))

    def tasks_by_status(self, target):
        if target not in STATUS_ORDER:
            raise ValueError(f"target must be one of {STATUS_ORDER}")
        result = []
        for task in self.tasks:
            current = self._task_status(task)
            if current == target:
                result.append(task)
        return result

    def delete_task(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                return
        raise ValueError(f"no task named '{name}' was found in this component")

    def report(self):
        return {task.name: self._task_status(task) for task in self.tasks}

    def to_dict(self):
        return {
            "name": self.name,
            "has_meter": self.has_meter,
            "meter_reading": self.meter_reading,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod 
    def from_dict(cls, data):
        component =  cls(data["name"], data["has_meter"], data["meter_reading"])
        for task_data in data["tasks"]:
            component.add_task(task_from_dict(task_data))
        return component
        

