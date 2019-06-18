import logging
import time
import threading
from threading import Thread
import ctypes

class PyThread(Thread):
    """
    Description: Custom thread class to get the return value from thread
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name, args=args,
                        kwargs=kwargs, verbose=verbose)
        self.__retval = None
        self.__duration = 0
        self.__cleanupFunc = None
        self.__abort = None
        self.exception = None
        self.stopped = False

    def run(self):
        """
        Description: Run a thread and save return value of the method executing as a thread
        """
        startTime = time.time()
        try:
            logging.debug("Starting thread '{}'".format(self.name))
            self.__retval = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            return self.__retval
        except SystemExit:
            logging.debug("SystemExit exception detected in thread - {}".format(self.name))
            self.exception = SystemExit
            self.stopped = True
        except Exception as ex:
            logging.error("An exception is raised in thread - {}".format(self.name))
            self.exception = ex
            self.stopped = True
        finally:
            stopTime = time.time()
            self.__duration = stopTime - startTime
            # If cleanup function is registered for thread, call cleanup function
            if self.__cleanupFunc:
                logging.debug("Executing cleanup function - '{}' of thread "
                              "- '{}'".format(self.__cleanupFunc.__name__, self.name))
                try:
                    self.__cleanupFunc()
                    logging.debug("Executing thread cleanup function - {}".format(self.__cleanupFunc.__name__))
                except Exception as ex:
                    logging.error("Exception occurred while executing cleanup "
                                  "function of thread - '{}'. Error - {}".format(self.name, ex))

    @property
    def executionTime(self):
        return self.__duration

    def getId(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for threadId, thread in threading._active.items():
            if thread is self:
                return threadId

    def raiseException(self):
        thread_id = self.getId()
        logging.debug("Thread id: {}".format(thread_id))
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        logging.debug("res: {}".format(res))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        logging.debug("Raised an exception to stop thread - {}".format(self.name))

    def stop(self, timeout=10.0):
        """
        Description: Stop a thread
        """
        self.raiseException()
        self.join(timeout)
        if self.isAlive():
            # If abort function is registered, abort the blocking thread
            if self.__abort:
                try:
                    self.__abort()
                    logging.info("Successfully stopped thread - {}".format(self.name))
                except Exception as ex:
                    logging.error("Failed to stop thread - {}. Error - {}".format(self.name, ex))
            logging.error("Failed to stop thread - {}".format(self.name))
        else:
            logging.info("Successfully stopped thread - {}".format(self.name))

    def getReturnValue(self):
        """
        Description: Return method's return value
        """
        return self.__retval

    def registerCleanupFunc(self, func):
        assert callable(func), "Can not register cleanup function. {} is not callable".format(func)
        self.__cleanupFunc = func

    def registerAbortFunc(self, func):
        assert callable(func), "Can not register abort function. {} is not callable".format(func)
        self.__abort = func
