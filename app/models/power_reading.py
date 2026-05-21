class powerReading:
    def __init__(self,station_id,building_id,reading_type,value,unit):       
        # Ex. Station where the power reading was captured from
        self.station_id: str = station_id
        # What building the power station is located in
        self.building_id: str = building_id
        # Ex. current, voltage, power
        self.reading_type: str = reading_type
        # Ex. amp, volt, watt
        self.unit: str = unit
        # Ex. 100, 200, 300
        self.value: float = value
    # To string method. Ex. print(powerReading) will print "amp/s: 100"
    def __str__(self):
        return f"{self.unit}/s: {self.value}"