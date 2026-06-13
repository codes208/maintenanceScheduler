from datetime import date
from dateutil.relativedelta import relativedelta

# Add helper function to get rid of the duplicate code for the non-negative values, and cannot log dates into the future

VALID_UNITS = ("miles", "hours")

class Task():
    def __init__(self, name):
        self.name = name

    def maintenance_due(self):
        raise NotImplementedError("Subclasses must implement maintenance_due()")

    def service_update(self, update_service):
        raise NotImplementedError("Subclasses must implement service_update()")


class MeteringTask(Task):
    def __init__(self, name, interval, last_serviced, unit, current_reading, warning_buffer=0):
        self._metering_validate(interval, last_serviced, unit, current_reading, warning_buffer)
        super().__init__(name)
        self.interval = interval
        self.last_serviced = last_serviced
        self.unit = unit
        self.current_reading = current_reading
        self.warning_buffer = warning_buffer

    def _require_non_negative(self, value, name):
        if value < 0:
            raise ValueError(f"{name} cannot be negative (got {value})")

    def _require_serviced_not_after_reading(self, serviced, reading):
        if serviced > reading:
            raise ValueError(f"last_serviced ({serviced}) cannot be greater than current_reading ({reading})")

    def _require_positive(self, value, name):
        if value <= 0:
            raise ValueError(f"{name} must be positive (got {value})")

    def _metering_validate(self, interval, last_serviced, unit, current_reading, warning_buffer):
        if unit not in VALID_UNITS:
            raise ValueError(f"unit must be one of the following: {VALID_UNITS}")
        self._require_positive(interval, "interval")
        self._require_non_negative(last_serviced, "last_serviced")
        self._require_non_negative(current_reading, "current_reading")
        self._require_non_negative(warning_buffer, "warning_buffer")
        self._require_serviced_not_after_reading(last_serviced, current_reading)

    def maintenance_due(self):
        elapsed = self.current_reading - self.last_serviced
        if elapsed >= self.interval:
            return "overdue"
        elif elapsed >= self.interval - self.warning_buffer:
            return "due_soon"
        else:
            return "ok"

    def service_update(self, update_service):
        self._require_non_negative(update_service, "update_service")
        self._require_serviced_not_after_reading(update_service, self.current_reading)
        self.last_serviced = update_service

    def reading_update(self, new_reading):
        self._require_non_negative(new_reading, "new_reading")
        self._require_serviced_not_after_reading(self.last_serviced, new_reading)
        self.current_reading = new_reading


class CalendarTask(Task):
    def __init__(self, name, interval, last_serviced, warning_buffer):
        self._calendar_validate(interval, last_serviced, warning_buffer)
        super().__init__(name)
        self.interval = interval #days/month/year
        self.last_serviced = last_serviced #date
        self.warning_buffer = warning_buffer #days/month/year

    def _calendar_validate(self, interval, last_serviced, warning_buffer):
        if not isinstance(last_serviced, date):
            raise TypeError("last_serviced must be of type date")
        if not isinstance(interval, relativedelta):
            raise TypeError("interval must be of type relativedelta")
        if not isinstance(warning_buffer, relativedelta):
            raise TypeError("warning_buffer must be of type relativedelta")
        if last_serviced > date.today():
            raise ValueError(f"last_serviced cannot be in the future (got {last_serviced})")

    def maintenance_due(self):
        due_date = self.last_serviced + self.interval
        warn_date = due_date - self.warning_buffer
        today = date.today()
        if today >= due_date:
            return "overdue"
        elif today >= warn_date:
            return "due_soon"
        else:
            return "ok"

    def service_update(self, update_service):
        if not isinstance(update_service, date):
            raise TypeError("service date must be of type date (yr/mth/day)")
        if update_service > date.today():
            raise ValueError(f"The service date cannot be in the future (got {update_service})")
        self.last_serviced = update_service

