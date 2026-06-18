from component import Component
import component
from task import STATUS_ORDER

# Add a report function that lists everything and that status nest dictonary
# Add a delete component function

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

    def delete_component(self, name):
        for component in self.components:
            if component.name == name:
                self.components.remove(component)
                return
        raise ValueError(f"no component named '{name}' was found in this asset")

    def report(self):
        return {component.name: component.report() for component in self. components}

