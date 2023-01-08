import unittest
from dbconnect import dbconnect
from PlanningApplication import PlanningApplication

# Test out the ability to accurately update planning application data

class TestPlanningApplication(unittest.TestCase):
    def test_update(self):
        """Check to confirm that old data in the database is replaced by more recent data"""
        db = dbconnect()
        db.connect()
        # Create a test example to be overwritten
        # Values to be updated: status, decision, decision_date, appeal, appeal_status, date_collected
        old_app = PlanningApplication()
        old_app.reference = "Test1"
        old_app.status = "old"
        old_app.decision = "old"
        old_app.decision_date = "9998-12-31"
        old_app.appeal = "old"
        old_app.appeal_status = "old"
        old_app.sendToDatabase(db.connection)
        # Create a newer value to overwrite
        new_app = PlanningApplication()
        new_app.reference = "Test1"
        new_app.status = "new"
        new_app.decision = "new"
        new_app.decision_date = "9999-12-31"
        new_app.appeal = "new"
        new_app.appeal_status = "new"
        new_app.sendToDatabase(db.connection)
        con.cursor.execute("select * from applications where Reference = 'Test1'")
        results = con.cursor.fetchall()
        print(results)
        #self.assertEqual() 
    # def test_update_submitted():
    #     """A 'submitted' record shall be updated by elements of a 'decided' record"""


if __name__ == "__main__":
    unittest.main()