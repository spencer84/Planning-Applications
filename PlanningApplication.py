
class PlanningApplication:
    def __init__(self):
        self.reference = None
        self.alt_reference = None
        self.date_received = None
        self.address = None
        self.proposal = None
        self.status = None
        self.appeal = None
        self.appeal_status = None
    def printAttributes(self):
        print(
            f"""Reference Number: {self.reference} 
            Alternative Ref Number: {self.alt_reference}
            Date Received: {self.date_received}
            Address: {self.address}
            Proposal: {self.proposal}
            Status: {self.status}
            Appeal: {self.appeal}
            Appeal Status: {self.appeal_status}
            """
        )
    #     self.db =
    # def sendToDatabase(self):