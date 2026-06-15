import unittest
from task import MeteringTask

#MeteringTask(name, interval, last_serviced, unit, warning_buffer=0):

class TestMeteringTask(unittest.TestCase):
    def test_over_due(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 50)
        self.assertEqual(task.maintenance_due(1700), "overdue")

    def test_due_soon(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 50)
        self.assertEqual(task.maintenance_due(1650), "due_soon")

    def test_ok(self):
        task = MeteringTask("Oil Change", 500, 1200, "hours", 50)
        self.assertEqual(task.maintenance_due(1250), "ok")

    def test_rejects_bad_unit(self):
        with self.assertRaises(ValueError):
            MeteringTask("Oil Change", 500, 0, "kilometers", 100)

    def test_service_update_zero_succeeds(self):
        task = MeteringTask("Oil Change", 500, 1200, "miles", 50)
        task.service_update(0, 1500)
        self.assertEqual(task.last_serviced, 0)

    def test_service_update_above_reading_raises(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 50)
        with self.assertRaises(ValueError):
            task.service_update(1600, 1500)

    # service_update(update_service, meter_reading=None):
    def test_update_climbs_update(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 50)
        task.service_update(1700, 1800)
        self.assertEqual(task.last_serviced, 1700)

