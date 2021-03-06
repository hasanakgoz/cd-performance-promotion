import unittest
import xmlrunner
import sys
import os
from cd_perf_promotion.engines.configengine import ConfigEngine
from cd_perf_promotion.engines.dataengine   import DataEngine

class TestSuite(unittest.TestCase):

    def test_no_appdynamics_connection(self):
        # Grab the configuration information
        configengine = ConfigEngine("./test_configs/config_test1.json", None, None, None, None, None, None, None, None)
        config_data = configengine.process_config()

        # Grab the performance data
        dataengine = DataEngine()

        # Check for a system exit call
        with self.assertRaises(SystemExit) as cm:
            dataengine.get_data(config_data)

        # Make sure that sys.exit(1) is called
        self.assertEqual(cm.exception.code, 1)

    def test_no_blazemeter_connection(self):
        # Grab the configuration information
        configengine = ConfigEngine("./test_configs/config_test2.json", None, None, None, None, None, None, None, None)
        config_data = configengine.process_config()

        # Grab the performance data
        dataengine = DataEngine()

        # Check for a system exit call
        with self.assertRaises(SystemExit) as cm:
            dataengine.get_data(config_data)

        # Make sure that sys.exit(1) is called
        self.assertEqual(cm.exception.code, 1)

    def test_no_webpagetest_connection(self):
        # Grab the configuration information
        configengine = ConfigEngine("./test_configs/config_test3.json", None, None, None, None, None, None, None, None)
        config_data = configengine.process_config()

        # Grab the performance data
        dataengine = DataEngine()

        # Check for a system exit call
        with self.assertRaises(SystemExit) as cm:
            dataengine.get_data(config_data)

        # Make sure that sys.exit(1) is called
        self.assertEqual(cm.exception.code, 1)

    def test_bad_webpagetest_location(self):
        # Grab the configuration information
        configengine = ConfigEngine("./test_configs/config_test3.json", None, None, None, None, None, None, None, None)
        config_data = configengine.process_config()

        # Grab the performance data
        dataengine = DataEngine()

        # Check for a system exit call
        with self.assertRaises(SystemExit) as cm:
            dataengine.get_data(config_data)

        # Make sure that sys.exit(1) is called
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
