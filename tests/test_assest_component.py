import unittest 
from asset import Asset, Component
from task import CalendarTask, MeteringTask

class TestComponent(unittest.TestCase):
    def test_components_instance(self):
        compressor = Component("Compressor#1", True, 1500)
        name_hours = (compressor.name, compressor.meter_reading)
        self.assertEqual(name_hours, (compressor.name, compressor.meter_reading))

    def test_meter_update_climb_succeeds(self):
        comp = Component("Compressor #1", True, 12000)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.meter_update(12500)
        self.assertEqual(12500, comp.meter_reading)

    def test_meter_update_below_highest_services_raises(self):
        comp = Component("Compressor #1", True, 1200)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.add_task(MeteringTask("Bearing lube", 2000, 11800, "hours", 100))
        with self.assertRaises(ValueError):
            comp.meter_update(11700)

    def test_meter_update_negative_raises(self):
        comp = Component("Compressor #1", True, 1200)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.add_task(MeteringTask("Bearing lube", 2000, 11800, "hours", 100))
        with self.assertRaises(ValueError):
            comp.meter_update(-11700)

    def test_meter_update_non_metering_tasks_uses_default(self):
        comp = Component("HVAC", True, 0)
        comp.meter_update(100)

        

