import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.shelley.poll import Poller

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.shelley_address = "AA:BB:CC:DD:EE:FF"
    return cfg


@pytest.fixture
def poller(config):
    return Poller(config)

@pytest.mark.asyncio
async def test_setup_device_sends_expected_sequence(poller):
    poller.call = AsyncMock()

    with patch("asyncio.sleep", new=AsyncMock()):
        await poller.setup_device()

    assert poller.call.await_count == 3

    poller.call.assert_any_await(
        poller.ADDRESS,
        "Switch.GetConfig",
        {"id": 0},
        100,
    )

    poller.call.assert_any_await(
        poller.ADDRESS,
        "Switch.SetConfig",
        {
            "id": 0,
            "config": {
                "in_mode": "detached",
                "initial_state": "on",
            },
        },
        200,
    )

    poller.call.assert_any_await(
        poller.ADDRESS,
        "Switch.Set",
        {"id": 0, "on": True},
        300,
    )
