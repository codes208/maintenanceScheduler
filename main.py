import json
from datetime import date
from dateutil.relativedelta import relativedelta
from task import MeteringTask, CalendarTask
from asset import Asset
from component import Component

# TODO CLI: warn when service_update value is below current last_serviced (legal but unusual — likely a typo)
# CalendarTask(name, interval, last_serviced, warning_buffer):
# MeteringTask(name, interval, last_serviced, unit, warning_buffer=0)

if __name__ == "__main__":
    refrigeration_system = Asset("Refrigeration System")

    compressor_1 = Component("Compressor #1", True, 12480)
    compressor_1.add_task(MeteringTask("Oil change", 500, 12000, "hours", 50))
    compressor_1.add_task(CalendarTask("Vibration analysis", relativedelta(months=3),
                                     date.today() - relativedelta(months=2), relativedelta(weeks=1)))

    evap_1 = Component("EVAP1")
    evap_1.add_task(CalendarTask("Check fan blades", relativedelta(months=1), date.today() - relativedelta(days=28), relativedelta(weeks=1)))
    evap_1.add_task(CalendarTask("Check drip pan", relativedelta(months=1), date.today() - relativedelta(days=28), relativedelta(weeks=1)))

    refrigeration_system.add_component(compressor_1)
    refrigeration_system.add_component(evap_1)

    print(f"Asset: {refrigeration_system.name}")
    for component in refrigeration_system.components:
        print(f" Component: {component.name} (meter: {component.meter_reading})")
        for task in component.tasks:
            status = task.maintenance_due(component.meter_reading)
            print(f"    {task.name}: {status}")
