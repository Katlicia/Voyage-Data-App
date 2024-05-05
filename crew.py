class Crew:
    def __init__(self, crew_id, first_name, last_name, address, nationality, birth_date, hire_date, role):
        self.crew_id = crew_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.nationality = nationality
        self.birth_date = birth_date
        self.hire_date = hire_date
        self.role = role

    def getCrewId(self):
        return self.crew_id

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
    
    def getRole(self):
        return self.role