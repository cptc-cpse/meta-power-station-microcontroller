import asyncio
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import ShelleyMethod
from app.shelley.poller import ShelleyPoller


class DummyClient:
    async def request(self, method, params=None):
        return {"method": method, "params": params}


class PollerTest(unittest.TestCase):
    def test_poll_once_collects_multiple_methods(self):
        methods = [
            ShelleyMethod(name="Switch.GetStatus", params={"id": 0}, topic_key="status"),
            ShelleyMethod(name="Switch.GetConfig", params={"id": 0}, topic_key="config"),
        ]
        poller = ShelleyPoller(methods, interval_s=5)
        client = DummyClient()

        result = asyncio.run(poller.poll_once(client))

        self.assertIn("status", result)
        self.assertIn("config", result)
        self.assertEqual(result["status"]["method"], "Switch.GetStatus")
        self.assertEqual(result["config"]["method"], "Switch.GetConfig")


if __name__ == "__main__":
    unittest.main()
