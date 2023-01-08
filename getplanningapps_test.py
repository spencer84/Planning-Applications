import unittest
import dbconnect
from PlanningApplication import PlanningApplication

# Test out the ability to accurately update planning application data

class TestPlanningApplication(unittest.TestCase):
    def test_update():
        """Check to confirm that old data in the database is replaced by more recent data"""
        con = dbconnect.dbconnect()
        # Create a test example to be overwritten
        # Values to be updated: status, decision, decision_date, appeal, appeal_status, date_collected
        old_app = PlanningApplication()
        old_app.reference = "Test1"
        old_app.status = "old"
        old_app.decision = "old"
        old_app.decision_date = "9998-12-31"
        old_app.appeal = "old"
        old_app.appeal_status = "old"
        old_app.sendToDatabase(con)
        # Create a newer value to overwrite
        new_app = PlanningApplication()
        new_app.reference = "Test1"
        new_app.status = "new"
        new_app.decision = "new"
        new_app.decision_date = "9999-12-31"
        new_app.appeal = "new"
        new_app.appeal_status = "new"
        new_app.sendToDatabase(con)
        
    def test_update_submitted():
        """A 'submitted' record shall be updated by elements of a 'decided' record"""


if __name__ == "__main__":
    unittest.main()