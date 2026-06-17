from component import Component
from task import STATUS_ORDER

class Asset:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        if not isinstance(component, Component):
            raise TypeError("component must be a Component instance")
        for existing in self.components:
            if existing.name == component.name:
                raise ValueError(f"a component named '{component.name}' already exists in this asset")
        self.components.append(component)

    def status(self):
        if not self.components:
            return "ok"
        statuses = []
        for component in self.components:
            statuses.append(component.status())
        return max(statuses, key=lambda s: STATUS_ORDER.index(s))

    def components_by_status(self, target):
        if target not in STATUS_ORDER:
            raise ValueError(f"target must be one of {STATUS_ORDER}")
        result = {}
        for component in self.components:
            matching = component.tasks_by_status(target)
            if matching:
                result[component.name] = matching
        return result


