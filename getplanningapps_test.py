import unittest
import dbconnect
from PlanningApplication import PlanningApplication

# Test out the ability to accurately update planning application data

class TestPlanningApplication(unittest.TestCase):
    def test_update():
        """Check to confirm that old data in the database is replaced by more recent data"""
        new_app = PlanningApplication()
    def test_update_submitted():
        """A 'submitted' record shall be updated by elements of a 'decided' record"""


if __name__ == "__main__":
    unittest.main()