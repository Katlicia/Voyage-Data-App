class Voyage:
    def __init__(self, voyage_id, departure_date, return_date, departure_harbor):
        self.voyage_id = voyage_id
        self.departure_date = departure_date
        self.return_date = return_date
        self.departure_harbor = departure_harbor

    def getVoyageId(self):
        return self.voyage_id
    
    def getDepartureDate(self):
        return self.departure_date
    
    def getReturnDate(self):
        return self.return_date
    
    def getDepartureHarbor(self):
        return self.departure_harbor