from threading import Timer

class RepeatedTimer:
    def __init__(self, interval, fn, *args):
        self._timer = None
        self.interval = interval
        self.fn = fn
        self.args = *args
        
        self.is_running = False
        self.start()
        
        self.bus = {}
        
    def _run(self):
        self.is_running = False
        self.start()
        self.fn(*self.args)
        
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
            
    def stop(self):
        self._timer.cancel()
        self.is_running = False
        
    #def access_bus(self):
        