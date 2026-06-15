import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from asset import Asset, Component
from task import CalendarTask, MeteringTask

class TestComponent(unittest.TestCase):
    def test_construction_stored_values(self):
        compressor = Component("Compressor#1", True, 1500)
        self.assertEqual(compressor.name, "Compressor#1")
        self.assertTrue(compressor.has_meter)
        self.assertEqual(compressor.meter_reading, 1500)

    def test_meter_update_climb_succeeds(self):
        comp = Component("Compressor #1", True, 12000)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.meter_update(12500)
        self.assertEqual(12500, comp.meter_reading)

    def test_meter_update_below_highest_services_raises(self):
        comp = Component("Compressor #1", True, 12000)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.add_task(MeteringTask("Bearing lube", 2000, 11800, "hours", 100))
        with self.assertRaises(ValueError):
            comp.meter_update(11700)

    def test_meter_update_negative_raises(self):
        comp = Component("Compressor #1", True, 12000)
        comp.add_task(MeteringTask("Oil change", 500, 11500, "hours", 50))
        comp.add_task(MeteringTask("Bearing lube", 2000, 11800, "hours", 100))
        with self.assertRaises(ValueError):
            comp.meter_update(-11700)

    def test_meter_update_with_no_metering_tasks_succeeds(self):
        comp = Component("HVAC", True, 0)
        comp.meter_update(100)
        self.assertEqual(comp.meter_reading, 100)

    def test_unmetered_with_reading_raises(self):
        with self.assertRaises(ValueError):
            Component("HVAC", False, 5000)

    def test_meter_update_on_unmetered_raises(self):
        comp = Component("HVAC")
        with self.assertRaises(ValueError):
            comp.meter_update(100)

    def test_add_metering_task_to_unmetered_raises(self):
        comp = Component("HVAC")
        with self.assertRaises(ValueError):
            comp.add_task(MeteringTask("Oil Change", 500, 100, "hours", 50))

    def test_add_calendar_task_to_unmetered_succeeds(self):
        comp = Component("HVAC")
        comp.add_task(CalendarTask("Filter", relativedelta(months=3), date.today(), relativedelta(weeks=1)))
        self.assertEqual(len(comp.tasks), 1)

    def test_add_calendar_task_to_metered_succeeds(self):
        comp = Component("Compressor#1", True, 1500)
        comp.add_task(CalendarTask("Filter", relativedelta(months=3), date.today(), relativedelta(weeks=1)))
        self.assertEqual(len(comp.tasks), 1)


        

