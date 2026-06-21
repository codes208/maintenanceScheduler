import unittest
import tempfile, os
from dateutil.relativedelta import relativedelta
from datetime import date
from owner import Owner
from asset import Asset
from component import Component
from task import MeteringTask, CalendarTask
from persistence import save, load

class TestPersistence(unittest.TestCase):
    def _build_owner(self):
        owner = Owner("Cody")

        asset = Asset("Refrigeration System")
        c1 = Component("Compressor #1", True, 12000)
        oil_change_1 = MeteringTask("Oil Change", 500, 11000, "hours", 50) # overdue
        c1.add_task(oil_change_1)
        c2 = Component("Compressor #2", True, 12000)
        oil_change_2 = MeteringTask("Oil Change", 500, 10500, "hours", 50) # overdue
        c2.add_task(oil_change_2)
        evap_1 = Component("Evaporator #1")
        fan_inspection = CalendarTask("Fan blade inspection", relativedelta(months=3), date.today(), relativedelta(weeks=1)) # ok
        evap_1.add_task(fan_inspection)
        asset.add_component(c1)
        asset.add_component(c2)
        asset.add_component(evap_1)
        owner.add_asset(asset)

        asset2 = Asset("Car")
        tires = Component("Tires", True, 10000)
        rotation = MeteringTask("Rotate", 10000, 5000, "miles", 500)
        tires.add_task(rotation)
        engine = Component("Engine", True, 10000)
        oil_change = MeteringTask("Oil change", 5000, 7500, "miles", 1000)
        engine.add_task(oil_change)
        interior = Component("interior")
        clean = CalendarTask("Detail", relativedelta(months=1), date.today(), relativedelta(days=21))
        interior.add_task(clean)
        owner.add_asset(asset2)

        return owner


    def test_save_load_round_trip(self):
        owner = self._build_owner()
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            save(owner, path)
            loaded = load(path)
            self.assertEqual(loaded.report(), owner.report())
        finally:
            os.remove(path)

    def test_load_rejects_invalid_data(self):
        bad = {"name": "Cody", "assets": [{"name": "X", "components": [
        {"name": "C", "has_meter": False, "meter_reading": None, "tasks": [
            {"type": "metering", "name": "Oil", "interval": 500,
             "last_serviced": 100, "unit": "hours", "warning_buffer": 50}
            ]}
        ]}]}
        # metering task on a has_meter=False component -> should raise on rebuild
        with self.assertRaises(ValueError):
            Owner.from_dict(bad)

