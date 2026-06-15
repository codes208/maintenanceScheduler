from datetime import date
from dateutil.relativedelta import relativedelta


VALID_UNITS = ("miles", "hours")

class Task():
    def __init__(self, name):
        self.name = name

    def maintenance_due(self, meter_reading=None):
        raise NotImplementedError("Subclasses must implement maintenance_due()")

    def service_update(self, update_service, meter_reading=None):
        raise NotImplementedError("Subclasses must implement service_update()")


class MeteringTask(Task):
    def __init__(self, name, interval, last_serviced, unit, warning_buffer=0):
        self._metering_validate(interval, last_serviced, unit, warning_buffer)
        super().__init__(name)
        self.interval = interval
        self.last_serviced = last_serviced
        self.unit = unit
        self.warning_buffer = warning_buffer

    def _require_non_negative(self, value, name):
        if value < 0:
            raise ValueError(f"{name} cannot be negative (got {value})")

    def _require_positive(self, value, name):
        if value <= 0:
            raise ValueError(f"{name} must be positive (got {value})")

    def _metering_validate(self, interval, last_serviced, unit, warning_buffer):
        if unit not in VALID_UNITS:
            raise ValueError(f"unit must be one of the following: {VALID_UNITS}")
        self._require_positive(interval, "interval")
        self._require_non_negative(last_serviced, "last_serviced")
        self._require_non_negative(warning_buffer, "warning_buffer")

    def maintenance_due(self, meter_reading=None):
        if meter_reading is None:
            raise ValueError("A metering task requires a meter reading")
        elapsed = meter_reading - self.last_serviced
        if elapsed >= self.interval:
            return "overdue"
        elif elapsed >= self.interval - self.warning_buffer:
            return "due_soon"
        else:
            return "ok"

    def service_update(self, update_service, meter_reading=None):
        self._require_non_negative(update_service, "update_service")
        if update_service > meter_reading:
            raise ValueError(f"Service point ({update_service}) cannot exceed meter reading ({meter_reading})")
        self.last_serviced = update_service


class CalendarTask(Task):
    def __init__(self, name, interval, last_serviced, warning_buffer):
        self._calendar_validate(interval, last_serviced, warning_buffer)
        super().__init__(name)
        self.interval = interval #days/month/year
        self.last_serviced = last_serviced #date
        self.warning_buffer = warning_buffer #days/month/year

    def _calendar_validate(self, interval, last_serviced, warning_buffer):
        self._instance_check(last_serviced, date, "last_serviced")
        self._instance_check(interval, relativedelta, "interval")
        self._instance_check(warning_buffer, relativedelta, "warning_buffer")
        self._non_future_value(last_serviced, "last_serviced")

    def _non_future_value(self, value, name):
        if value > date.today():
            raise ValueError(f"{name} cannot be set in the future (got {value})")

    def _instance_check(self, value, expected_type, name):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be of type {expected_type.__name__}")

    def maintenance_due(self, meter_reading=None):
        due_date = self.last_serviced + self.interval
        warn_date = due_date - self.warning_buffer
        today = date.today()
        if today >= due_date:
            return "overdue"
        elif today >= warn_date:
            return "due_soon"
        else:
            return "ok"

    def service_update(self, update_service, meter_reading=None):
        self._instance_check(update_service, date, "update_service")
        self._non_future_value(update_service, "update_service")
        self.last_serviced = update_service

