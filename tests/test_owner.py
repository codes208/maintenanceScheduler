import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from owner import Owner
from asset import Asset
from component import Component
from task import MeteringTask, CalendarTask

class TestOwner(unittest.TestCase):
    def _overdue_asset(self, name):
        asset = Asset(name)
        comp = Component("Compressor #1", True, 12000)
        comp.add_task(MeteringTask("Oil change", 500, 11000, "hours", 50))   # overdue
        asset.add_component(comp)
        return asset

    def _ok_asset(self, name):
        asset = Asset(name)
        comp = Component("Evaporator #1")
        comp.add_task(CalendarTask("Fan inspection", relativedelta(months=3),
                                   date.today(), relativedelta(weeks=1)))     # ok
        asset.add_component(comp)
        return asset

    def test_empty_owner_status_is_ok(self):
        owner = Owner("Cody")
        self.assertEqual(owner.status(), "ok")

    def test_add_asset_rejects_non_asset(self):
        owner = Owner("Cody")
        with self.assertRaises(TypeError):
            owner.add_asset("not an asset")

    def test_add_duplicate_asset_name_raises(self):
        owner = Owner("Cody")
        owner.add_asset(Asset("Refrigeration System"))
        with self.assertRaises(ValueError):
            owner.add_asset(Asset("Refrigeration System"))

    def test_status_rolls_up_worst_asset(self):
        owner = Owner("Cody")
        owner.add_asset(self._ok_asset("Walk-in"))
        owner.add_asset(self._overdue_asset("Rack A"))
        self.assertEqual(owner.status(), "overdue")

    def test_assets_by_status_gathers_across_assets(self):
        owner = Owner("Cody")
        owner.add_asset(self._overdue_asset("Rack A"))
        owner.add_asset(self._ok_asset("Walk-in"))     # ok → excluded
        result = owner.assets_by_status("overdue")
        self.assertEqual(set(result.keys()), {"Rack A"})           # only the overdue asset
        self.assertIn("Compressor #1", result["Rack A"])           # nested structure intact

    def test_assets_by_status_rejects_bad_target(self):
        owner = Owner("Cody")
        with self.assertRaises(ValueError):
            owner.assets_by_status("ovrdue")

    def test_delete_asset_removes_it(self):
        owner = Owner("Cody")
        owner.add_asset(Asset("Refrigeration System"))
        owner.delete_asset("Refrigeration System")
        self.assertEqual(owner.assets, [])

    def test_delete_asset_missing_raises(self):
        owner = Owner("Cody")
        with self.assertRaises(ValueError):
            owner.delete_asset("Nonexistent")

    def test_report_nests_by_asset(self):
        owner = Owner("Cody")
        owner.add_asset(self._overdue_asset("Rack A"))
        expected = {
            "Rack A": {
                "Compressor #1": {"Oil change": "overdue"}
            }
        }
        self.assertEqual(owner.report(), expected)

    def test_owner_round_trip(self):
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

        rebuilt = Owner.from_dict(owner.to_dict())
        self.assertEqual(rebuilt.to_dict(), owner.to_dict())
