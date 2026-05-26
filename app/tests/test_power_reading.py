from app.models.power_reading import powerReading

import pytest

def test_power_reading_sets_attributes():
    reading = powerReading(
        station_id="station-1",
        building_id="building-1",
        reading_type="power",
        value=100,
        unit="watt",
    )

    assert reading.station_id == "station-1"
    assert reading.building_id == "building-1"
    assert reading.reading_type == "power"
    assert reading.value == 100
    assert reading.unit == "watt"


def test_power_reading_str():
    reading = powerReading(
        station_id="station-1",
        building_id="building-1",
        reading_type="current",
        value=200,
        unit="amp",
    )

    assert str(reading) == "amp/s: 200"
