import unittest
from datetime import date 
from dateutil.relativedelta import relativedelta
from component import CalendarTask

class TestCalendarTask(unittest.TestCase):
    def test_over_due(self):
        task = CalendarTask("Vibration Analysis", relativedelta(months=3), date(2026, 3, 1), relativedelta(weeks=1))
        self.assertEqual(task.maintenance_due(), "overdue")

    def test_due_soon(self):
        task = CalendarTask("Charge Battery", relativedelta(weeks=1), date(2026, 6, 7), relativedelta(days=3))
        self.assertEqual(task.maintenance_due(), "due_soon")

    def test_ok(self):
        task = CalendarTask("Oil Change", relativedelta(months=3), date(2026, 6, 11), relativedelta(weeks=1))
        self.assertEqual(task.maintenance_due(), "ok")

    def test_last_serviced_failure(self):
        with self.assertRaises(ValueError):
            CalendarTask("Test Breakers", relativedelta(months=3), date(2026, 9, 11), relativedelta(weeks=2))



