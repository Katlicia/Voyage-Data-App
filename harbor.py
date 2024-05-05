class Harbor:
    def __init__(self, harbor_name, country, population, requires_passport, docking_fee):  
        self.harbor_name = harbor_name
        self.country = country
        self.population = population
        self.requires_passport = requires_passport
        self.docking_fee = docking_fee

    def getHarborName(self):
        return self.harbor_name
    
    def getHarborCountry(self):
        return self.country
    
    def getHarborPopulation(self):
        return self.population
    
    def getPassportRequire(self):
        return self.requires_passport
    
    def getDockingFee(self):
        return self.docking_fee