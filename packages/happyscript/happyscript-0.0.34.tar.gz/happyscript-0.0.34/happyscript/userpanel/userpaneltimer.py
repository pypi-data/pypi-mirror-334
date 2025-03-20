from threading import Timer

class UserPanelTimer(object):
    def __init__(self, interval_source, function, *args, **kwargs):
        """interval timer that repeatedly calls a callback function 
        based on: https://stackoverflow.com/a/13151299

        Arguments:
            interval_source -- SmartInput object to retrieve the interval in seconds from 
            function -- callback function to run every interval
        """
        self._timer     = None
        self.interval_source   = interval_source
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
    
    def __run(self):
        """callback to run after timer completes
        """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    
    def start(self):
        """starts the timer
        """
        if not self.is_running:
            self._timer = Timer(self.interval_source.set(), self.__run)
            self._timer.start()
            self.is_running = True
    
    def restart(self):
        """restarts the timer
        """
        if self.is_running:
            self.stop()
        self.start()

    def stop(self):
        """stops the timer
        """
        if self._timer is not None:
            self._timer.cancel()
        self.is_running = False
