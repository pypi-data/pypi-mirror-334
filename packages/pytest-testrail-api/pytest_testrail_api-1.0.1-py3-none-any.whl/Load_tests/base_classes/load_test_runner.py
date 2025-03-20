import logging
import random
from typing import List, Type, Union

from gevent import spawn, spawn_later
from locust import User, stats
from locust.env import Environment


# TODO: To think about the inheritance from the Environment class
class LoadTestRunner(Environment):
    def __init__(self, user_classes: Union[Type[User], List[Type[User]]], host: str = None, reset_stats: bool = False):
        """
        Initialize a new instance of the class.

        Parameters:
        - user_classes: A list of User objects, or a single User object.
        - host: The default host to run the tests against. I came from the User objects in the user_classes or can be setup here
        - reset_stats: A flag indicating whether to reset the stats before the test run.
        """

        user_classes = user_classes if isinstance(user_classes, list) else [user_classes]

        super().__init__(user_classes=user_classes, host=host)

        self.reset_stats = reset_stats
        self.tests_results = None
        self.failure_summary = None
        self.create_local_runner()

        # Start a greenlet that periodically outputs the current stats
        spawn(stats.stats_printer, self.stats)

    def add_suite(self, test_suite):
        if test_suite not in self.user_classes:
            self.user_classes.append(test_suite)

    def run_test(self, number_of_users, test_duration, spawn_rate=None):
        assert self.user_classes, "Tests list is empty! Nothing to run!"

        # Turn OFF excess logging
        logging.disable(logging.CRITICAL)

        # Start a greenlet that periodically write stats_history to the current env object
        spawn(stats.stats_history, self.runner)
        # Set the spawn_rate depends on the
        spawn_rate = spawn_rate or round(random.uniform(number_of_users * 0.25, number_of_users * 0.75)) or 1

        try:
            self.runner.start(number_of_users, spawn_rate=spawn_rate)
            spawn_later(test_duration, lambda: self.runner.quit())
            self.runner.greenlet.join()
        except Exception as e:
            logging.error(f"Test run failed: {e}")
        finally:
            logging.info("Teardown: Stopping runner...")
            self.runner.stop()

        self.tests_results = self.runner.stats
        self.failure_report()

        return self

    def failure_report(self):
        """
        Generate a failure report.

        Returns:
        - A dictionary where the keys are (method, name) tuples representing endpoints,
          and the values are dictionaries with 'num_failures' and 'failure_rate'.
        """
        failure_report = {}

        for key, stats_entry in self.stats.entries.items():
            method, name = key
            num_failures = stats_entry.num_failures
            num_requests = stats_entry.num_requests
            failure_rate = round(100 * num_failures / num_requests, 2) if num_requests else 0

            if num_failures:
                failure_report[(method, name)] = {
                    "num_failures": num_failures,
                    "failure_rate": failure_rate,
                }

        if failure_report:
            self.failure_summary = failure_report

        return failure_report


if __name__ == "__main__":
    ...
