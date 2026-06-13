import unittest
from datetime import date 
from dateutil.relativedelta import relativedelta
from task import CalendarTask

# CalendarTask(name, interval, last_serviced, warning_buffer)

class TestCalendarTask(unittest.TestCase):
    def test_over_due(self):
        serviced = date.today() - relativedelta(months=6)
        task = CalendarTask("Vibration Analysis", relativedelta(months=3), serviced, relativedelta(weeks=1))
        self.assertEqual(task.maintenance_due(), "overdue")

    def test_due_soon(self):
        serviced = date.today() - relativedelta(months=3) + relativedelta(days=4)
        task = CalendarTask("Charge Battery", relativedelta(months=3), serviced, relativedelta(weeks=1))
        self.assertEqual(task.maintenance_due(), "due_soon")

    def test_ok(self):        
        task = CalendarTask("Oil Change", relativedelta(months=3), date.today(), relativedelta(weeks=1))
        self.assertEqual(task.maintenance_due(), "ok")

    def test_last_serviced_failure(self):
        serviced = date.today() + relativedelta(months=3)
        with self.assertRaises(ValueError):
            CalendarTask("Test Breakers", relativedelta(months=3), serviced, relativedelta(weeks=2))

    def test_service_update_today_succeeds(self):
        task = CalendarTask("Check temp cut out", relativedelta(months=3), date.today() - relativedelta(months=1), relativedelta(weeks=1))
        task.service_update(date.today())
        self.assertEqual(task.last_serviced, date.today())

    def test_service_update_future_raises(self):
        task = CalendarTask("Check oil level", relativedelta(days=1), date.today() - relativedelta(days=1), relativedelta(hours=18))
        with self.assertRaises(ValueError):
            task.service_update(date.today() + relativedelta(months=3))

    def test_service_update_wrong_type_raises(self):
        task = CalendarTask("Check air pressure", relativedelta(weeks=1), date.today(), relativedelta(days=5))
        with self.assertRaises(TypeError):
            task.service_update("2024, 05, 30")

    def test_init_future_serviced_raises(self):
        with self.assertRaises(ValueError):
            CalendarTask("Oil", relativedelta(months=3), date.today() + relativedelta(days=1), relativedelta(weeks=1))

    def test_init_wrong_interval_type_raises(self):
        with self.assertRaises(TypeError):
            CalendarTask("Oil", 90, date.today(), relativedelta(weeks=1))

    



