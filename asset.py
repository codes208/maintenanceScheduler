from component import Component

class Asset:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        if not isinstance(component, Component):
            raise TypeError("component must be a Component instance")
        self.components.append(component)

