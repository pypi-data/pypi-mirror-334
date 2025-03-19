import unittest
from gobbezlearningtoolbox.core import start

class TestStart(unittest.TestCase):
    def test_start(self):
        self.assertEqual(start(), "learningtoolbox active!")
