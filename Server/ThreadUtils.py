import threading

class ControlledThread(threading.Thread):
    """
    The ControlledThread is a controllable thread, meaning once started
    it can be paused, resumed and stopped. A class must inherit it overriding
    and implementing the do_work() method which will be called repeatedly
    in the thread running loop.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        # a count of how many times the loop has iterated
        self.iterations = 0
        # when program quits, daemon threads are killed automatically
        self.daemon = True
        self.paused = True  # start out paused
        self.stopped = False
        self._finished = False
        self.state = threading.Condition()

    def run(self):
        """ Called at ControlledThread.start(), start the main thread loop.
        :return:
        """
        self.resume() # unpause self
        while not self._finished:
            if self.condition() is False:
                return
            self.do_work()
            self.iterations += 1

    def resume(self):
        """ Resume the thread, automatically called at ControlledThread.start()
        :return:
        """
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def do_work(self):
        """ Do the thread work. When job done, call ControlledThread.finish()
        :return:
        """
        raise NotImplementedError

    def condition(self):
        """ Check the current thread condition.
        :return: Bool if should break the main thread loop.
        """
        with self.state:
            if self.paused:
                self.state.wait()   # block until notified
            if self.stopped:
                return False        # stop the execution
        return True

    def pause(self):
        """ Pause the thread
        :return:
        """
        with self.state:
            self.paused = True  # make self block and wait

    def stop(self):
        """ Stop the thread. Once stopped, it can not be resumed or started.
        :return:
        """
        with self.state:
            self.stopped = True
            self.paused = False
            self.state.notify()     # unblock if waiting

    def finish(self):
        """ Finish the thread breaking the thread loop condition.
        Should be called from ControlledThread.do_work() when job is done.
        :return:
        """
        self._finished = True
        self.stop()

    def finished(self):
        """ Whether the job was finished. Can be used to check if the thread
        was stopped manually or it normally exited.
        :return: if the worker finished
        """
        return self._finished