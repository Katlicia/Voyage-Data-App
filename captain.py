class Captain:
    def __init__(self, captain_id, first_name, last_name, address=None, nationality=None, birth_date=None, hire_date=None, license_type=None):
        self.captain_id = captain_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.nationality = nationality
        self.birth_date = birth_date
        self.hire_date = hire_date
        self.license_type = license_type

    def getCaptainID(self):
        return self.captain_id
    
    def getFirstName(self):
        return self.first_name
    
    def getLastName(self):
        return self.last_name
    
    def getAddress(self):
        return self.address
    
    def getNationality(self):
        return self.nationality
    
    def getBirthDate(self):
        return self.birth_date
    
    def getHireDate(self):
        return self.hire_date
    
    def getLicenseType(self):
        return self.license_type