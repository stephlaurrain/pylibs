import os
from os import path
import inspect

class Stopper:
      
    def __init__(self, root_app, trace, log):            
            self.trace = trace
            self.log = log            
            self.root_app = root_app

    def stop(self):
            self.trace(inspect.stack())
            stopfile = f"{self.root_app}{os.path.sep}stop"
            res = path.exists(stopfile)
            if (res):
                    self.log.lg("=STOP THE BOT=")
            return res
        
    def remove_stop(self):
        self.trace(inspect.stack())
        stopfile = f"{self.root_app}{os.path.sep}stop"
        res = path.exists(stopfile)
        if (res):
                os.remove(stopfile)