import unittest
import logging
import time
from unittest import TestCase
from pythread import PyThread

class QVSThreadTests(TestCase):

    def setUp(self):
        def foo(delay, iterations):
            logging.info("foo - Start")
            for val in range(iterations):
                time.sleep(delay)
            logging.info("foo - Done")
        self.target = foo

    def test_simple(self):
        """
        Check if basic thread functionality is working
        """
        delay = 1
        iterations = 10
        expectedExecutionTime = delay * iterations
        logging.debug("Expected execution time: {} seconds".format(expectedExecutionTime))
        thread = PyThread(target=self.target, args=(delay, iterations))
        thread.start()
        thread.join(15.0)
        self.assertFalse(thread.is_alive(), msg="CRITICAL: Thread did not exit in expected time")
        logging.debug("ExecutionTime: {}".format(thread.executionTime))
        self.assertAlmostEqual(thread.executionTime, expectedExecutionTime, delta=1,
                               msg="Thread took more than expected time")


    def test_stop_thread(self):
        """
        Check if stop thread functionality is working
        """
        delay = 1
        iterations = 10
        thread = PyThread(target=self.target, args=(delay, iterations))
        thread.start()
        time.sleep(1)
        thread.stop()
        self.assertFalse(thread.is_alive(), msg="CRITICAL: Failed to stop thread")
        self.assertEqual(thread.exception, SystemExit, msg="CRITICAL: SystemExit exception not raised on stop")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging started")
    unittest.main()

