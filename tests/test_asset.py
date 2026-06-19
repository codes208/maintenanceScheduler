import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from asset import Asset
from component import Component
from task import CalendarTask, MeteringTask

#MeteringTask(name, interval, last_serviced, unit, warning_buffer=0)

class TestAsset(unittest.TestCase):
    def test_asset_rolls_up_worst_component(self):
        
        asset = Asset("Refrigeration System")
        c1 = Component("Compressor #1", True, 12000)
        c1.add_task(MeteringTask("Oil Change", 500, 11900, "hours", 50)) # ok
        c2 = Component("Compressor #2", True, 12000)
        c2.add_task(MeteringTask("Oil Change", 500, 11000, "hours", 50)) # overdue
        asset.add_component(c1)
        asset.add_component(c2)
        self.assertEqual(asset.status(), "overdue")

    def test_components_by_status_gathers_across_components(self):
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
        result = asset.components_by_status("overdue")
        self.assertEqual(set(result.keys()), {"Compressor #1", "Compressor #2"})
        self.assertEqual(result["Compressor #1"], [oil_change_1])
        self.assertEqual(result["Compressor #2"], [oil_change_2])

    def test_add_duplicate_component_name_raises(self):
        asset = Asset("Refrigeration System")
        asset.add_component(Component("Compressor #1", True, 12000))
        with self.assertRaises(ValueError):
            asset.add_component(Component("Compressor #1", True, 8000))
        

class TestReport(unittest.TestCase):
    def test_asset_report_nests_by_component(self):
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
        self.assertEqual(
            asset.report(), 
            {
                "Compressor #1": {"Oil Change": "overdue"},
                "Compressor #2": {"Oil Change": "overdue"},
                "Evaporator #1": {"Fan blade inspection": "ok"}
            }
        )

class TestDeletion(unittest.TestCase):
    def test_delete_component_removes_it(self):
        asset = Asset("Refrigeration System")
        asset.add_component(Component("Compressor #1", True, 12000))
        asset.delete_component("Compressor #1")
        self.assertEqual(asset.components, [])

    def test_delete_component_missing_raised(self):
        asset = Asset("Refrigeration System")
        with self.assertRaises(ValueError):
            asset.delete_component("Nonexistent")


