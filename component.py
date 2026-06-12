VALID_INTERVALS = ("miles", "hours", "days") 

class Component():
    def __init__(self, name, interval_type, interval, current_reading=0, last_serviced=0, warning_buffer=0):
        if interval_type not in VALID_INTERVALS:
            raise ValueError(f"interval_type must be one of the following: {VALID_INTERVALS}")
        self.name = name
        self.interval_type = interval_type
        self.interval = interval
        self.current_reading = current_reading
        self.last_serviced = last_serviced
        self.warning_buffer = warning_buffer


