"""measureData が errorCode を返したときの警告ログを検証する。"""

from __future__ import annotations

import unittest
from unittest import mock

from app.client import OmronConnectV1

DEVICE = {"deviceCategory": "0", "deviceSerialID": "SN1", "userNumberInDevice": "1"}


class MeasurementErrorCodeTest(unittest.TestCase):
    def test_error_code_logs_warning_and_returns_empty(self):
        client = OmronConnectV1()
        response = mock.Mock()
        response.json.return_value = {"returnedValue": {"errorCode": "SYNTHETIC\nFAILURE"}}
        client._session = mock.Mock()
        client._session.post.return_value = response

        with self.assertLogs("app.client", level="WARNING") as logs:
            result = client.get_measurements(DEVICE)

        self.assertEqual(result, [])
        self.assertEqual(len(logs.records), 1)
        message = logs.records[0].getMessage()
        self.assertIn("SYNTHETIC", message)
        self.assertNotIn("\n", message)


if __name__ == "__main__":
    unittest.main()
