import os
from os import path
import inspect

class Bot_utils:
      
    def __init__(self, trace, log, jsprms):            
            self.trace = trace
            self.log = log
            self.jsprms = jsprms

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