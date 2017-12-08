from unittest import TestCase

import pystat

class TestPystat(TestCase):

  def setUp(self):
    """Init"""

  def test_get_versions(self):
    self.assertEqual(pystat.get_versions("student", "\d+\.\d+\.\d+"), ['3.6.3', '2.7.14'])
