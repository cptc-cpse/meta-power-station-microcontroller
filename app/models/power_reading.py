from dataclasses import dataclass

@dataclass
class PowerReading:
    station_id: str
    building_id: str
    reading_type: str
    value: float
    unit: str

    def __str__(self):
        return f"{self.unit}/s: {self.value}"