import requests
import xmltodict
import json
import time
from cd_perf_promotion.modules.perftools import PerfTools

class WebPageTest(PerfTools):
    """
    Handles all of the WebPageTest API querying/data gathering
    """

    def __init__(self, url, location, api_key):
        """
        Sets up all of the instance variables

        Keyword arguments:
        api_key      - The WebPageTest API key (string)
        test_session - The WebPageTest Test ID (string)
        """
        # Test configuration information
        self.url = url
        self.location = location
        self.api_key = api_key
        # Inherit methods from parent class "PerfTools"
        PerfTools.__init__(self, "WebPageTest")

    def run_test(self, url, runs, location, api_key):
        """
        Runs the UI test
        """
        # Run performance test (HTTP GET request)
        run_test_url = "http://www.webpagetest.org/runtest.php?url={0}&runs={1}&f=json&location={2}&k={3}".format(url, runs, location, api_key)
        try:
            run_test_request = requests.get(run_test_url)
        except:
            self.connection_error() # Inherited from the parent class

        # Make sure that the module actually got something back
        # Covers cases where users enter crazy parameters or WebPageTest miraculously
        # determines your query is bad
        if (run_test_request.status_code != 200) or (run_test_request.json()["statusCode"] != 200):
            self.connection_error() # Inherited from the parent class

        # Get the test ID so that we can look at the results later
        test_id = run_test_request.json()["data"]["testId"]

        # Let the user know what's going on
        print("Queued WebPageTest UI test")
        return test_id

    def get_data(self):
        """
        Gets the load test data from the API
        """
        # Run the test ad get the Test ID
        # Use two runs for now. Unforunately, the WebPageTest API stores the runs as individual objects
        # as part of a larger run object instead of as an array of run objects. You can track this
        # issue further here: https://github.com/WPO-Foundation/webpagetest/issues/475
        # This is slightly relieved by xmltodict's conversion to JSON, which does turn it into
        # an array if there is more than one run object. Until a workaround can be completed, just
        # do two runs :-/
        test_id = self.run_test(self.url, 2, self.location, self.api_key)

        # Wait until the test results are ready
        checkStatusCode = 100
        timePassed = 0
        testStatus = ""
        while (checkStatusCode != 200):
            if (timePassed > 600):
                # 10 minutes have passed, error out. Something probably went wrong.
                #self.connection_error() # Inherited from the parent Class
                print("timepassed broke")
            else:
                # Check the test results
                test_summary_url = "http://www.webpagetest.org/xmlResult/{0}/".format(test_id)
                try:
                    test_summary_request = requests.get(test_summary_url)
                except:
                    self.connection_error() # Inherited from the parent class

                # Are the test results ready?
                # Have to do some string to int conversions due to the XML stuff
                if ((test_summary_request.status_code == 200) and
                     (int(json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))["response"]["statusCode"]) == 200)):
                    # Yes, break the loop and
                    checkStatusCode = 200
                elif ((test_summary_request.status_code == 200) and
                      ((int(json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))["response"]["statusCode"]) < 200) and
                       (int(json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))["response"]["statusCode"]) >= 100))):
                    # Let the user know when the test has been started
                    newStatus = json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))["response"]["statusText"]
                    if newStatus != testStatus:
                        if (newStatus == "Test Started"):
                            print("Started WebPageTest UI test")
                        testStatus = newStatus
                    # Be nice to the WebPageTest API
                    time.sleep(10)
                    timePassed += 10
                else:
                    # Something broke
                    self.connection_error() # Inherited from the parent class

        # Convert all of the WebPageTest data from XML to JSON and return it
        test_results = json.loads(json.dumps(xmltodict.parse(test_summary_request.content)))

        # Notify the user that the WebPageTest data is being grabbed
        print("Retrieved WebPageTest data")

        return test_results
