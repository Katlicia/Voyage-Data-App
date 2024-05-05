class Ship:
    def __init__(self, ship_id, ship_name, ship_type, ship_weight, construction_year, passenger_capacity=None, max_weight=None, container_capacity = None, oil_capacity=None):
        self.ship_id = ship_id
        self.ship_name = ship_name
        self.ship_weight = ship_weight
        self.construction_year = construction_year
        self.ship_type = ship_type
        self.passenger_capacity = passenger_capacity
        self.max_weight = max_weight
        self.container_capacity = container_capacity
        self.oil_capacity = oil_capacity

    def getShipId(self):
        return self.ship_id

    def getShipName(self):
        return self.ship_name
    
    def getShipWeight(self):
        return self.ship_weight
    
    def getShipConstructionYear(self):
        return self.construction_year
    
    def getShipType(self):
        return self.ship_type
    
    def getPassengerCapacity(self):
        return self.passenger_capacity
    
    def getMaxWeight(self):
        return self.max_weight
    
    def getContainerCapacity(self):
        return self.container_capacity
    
    def getOilCapacity(self):
        return self.oil_capacity
    
    def printShip(self):
        print(self.ship_id, self.ship_name, self.ship_type, self.ship_weight, self.construction_year, self.passenger_capacity, self.container_capacity, self.oil_capacity, self.max_weight)