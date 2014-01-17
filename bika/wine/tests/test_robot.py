from bika.wine.testing import BIKAWINE_ROBOT_TESTING
from plone.testing import layered
from pkg_resources import resource_listdir
import robotsuite
import unittest


robots = [f for f in resource_listdir("bika.wine", "tests")
          if f.endswith(".robot")]


def test_suite():
    suite = unittest.TestSuite()
    for robot in robots:
        suite.addTests([
            layered(robotsuite.RobotTestSuite(robot), layer=BIKAWINE_ROBOT_TESTING),
        ])
    return suite
