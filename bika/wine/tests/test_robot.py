from bika.debortoli.testing import BIKA_DEBORTOLI_TESTING
from plone.testing import layered

import robotsuite
import unittest


ROBOT_TESTS = [
    'test_debortoli.robot',
]


def test_suite():
    suite = unittest.TestSuite()
    for RT in ROBOT_TESTS:
        suite.addTests([
            layered(robotsuite.RobotTestSuite(RT), layer=BIKA_DEBORTOLI_TESTING),
        ])
    return suite
