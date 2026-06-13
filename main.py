from datetime import date
from dateutil.relativedelta import relativedelta
from component import Component, MeteringTask, CalendarTask

if __name__ == "__main__":
    compressor = Component("Compressor #1")
    compressor.add_task(MeteringTask("Oil change", 500, 12000, "hours", 12480, 50))
    compressor.add_task(CalendarTask("Vibration analysis", relativedelta(months=3),
                                     date(2026, 3, 20), relativedelta(weeks=1)))
    for task in compressor.tasks:
        print(f"{task.name}: {task.maintenance_due()}")
