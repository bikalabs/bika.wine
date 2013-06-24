from bika.wine.testing import BIKA_ROBOT_TESTING
from plone.testing import layered

import robotsuite
import unittest


ROBOT_TESTS = [
    'test_wine.robot',
]


def test_suite():
    suite = unittest.TestSuite()
    for RT in ROBOT_TESTS:
        suite.addTests([
            layered(robotsuite.RobotTestSuite(RT), layer=BIKA_ROBOT_TESTING),
        ])
    return suite
