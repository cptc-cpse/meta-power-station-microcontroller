from app.configuration import config as app_config
from app.mqtt import publisher as mqtt_publisher
def test_publisher_initializes_with_config():
    config = app_config.get_config()
    publisher = mqtt_publisher.Publisher(config)

    assert publisher.BROKER == config.mqtt_broker_address
    assert publisher.PORT == config.mqtt_broker_port
    assert publisher.QOS == config.mqtt_qos
    assert publisher.RETAIN == config.mqtt_retain
    assert publisher.LAST_WILL_MESSAGE == f"{config.station_id} in {config.building_id} has disconnected"
    assert publisher.LAST_WILL_TOPIC == f"clover_park/{config.building_id}/meta_power_station/{config.station_id}/status"

def test_publisher_publish_method():
    config = app_config.get_config()
    publisher = mqtt_publisher.Publisher(config)

    # This test currently only checks that the publish method executes without exceptions.
    # More comprehensive testing would require mocking, which I don't entirely get yet.
    try:
        publisher.publish("test/topic", '{"current": 5}')
        assert True, "Publish method executed without exceptions."
    except Exception as e:
        assert False, f"Publish method raised an exception: {e}"