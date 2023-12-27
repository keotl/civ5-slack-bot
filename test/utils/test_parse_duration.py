import unittest
from datetime import datetime, timedelta
from unittest import mock

from civbot.app.util.parse_duration import parse_duration


class ParseDurationTests(unittest.TestCase):

    def test_parse_string(self):
        timeout = parse_duration("10w1d1h", now)
        self.assertEqual(now + timedelta(days=71, hours=1), timeout)


now = datetime.now()
