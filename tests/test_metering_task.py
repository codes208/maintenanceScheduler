import unittest
from task import MeteringTask

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

    def test_service_update_zero_succeeds(self):
        task = MeteringTask("Oil Change", 500, 1200, "miles", 1500, 50)
        task.service_update(0)
        self.assertEqual(task.last_serviced, 0)

    def test_service_update_above_reading_raises(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 1500, 50)
        with self.assertRaises(ValueError):
            task.service_update(1600)

    def test_update_climbs_update(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 1500, 50)
        task.service_update(1400)
        self.assertEqual(task.last_serviced, 1400)

    def test_reading_update_climbs_succeeds(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 1500, 50)
        task.reading_update(1800)
        self.assertEqual(task.current_reading, 1800)

    def test_reading_update_below_serviced_raises(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 1500, 50)
        with self.assertRaises(ValueError):
            task.reading_update(1000)

    def test_reading_update_negative_raises(self):
        task = MeteringTask("Oil change", 500, 1200, "miles", 1500, 50)
        with self.assertRaises(ValueError):
            task.reading_update(-5)



