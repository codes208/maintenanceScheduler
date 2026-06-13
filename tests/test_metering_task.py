import unittest
from component import MeteringTask

class TestMeteringTask(unittest.TestCase):
    def test_over_due(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 12600, 50)
        self.assertEqual(task.maintenance_due(), "overdue")

    def test_due_soon(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 1650, 50)
        self.assertEqual(task.maintenance_due(), "due_soon")

    def test_ok(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 1250, 50)
        self.assertEqual(task.maintenance_due(), "ok")

    def test_rejects_bad_unit(self):
        with self.assertRaises(ValueError):
            MeteringTask("Oil Change", 500, 0, "kilometers", 100)
    
    def test_bad_last_serviced_value(self):
        with self.assertRaises(ValueError):
            MeteringTask("Oil Change", 500, 1100, "miles", 1000, 10)

