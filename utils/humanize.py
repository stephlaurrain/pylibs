import inspect
from time import sleep
import random
from utils.mydecorators import _error_decorator


class Humanize:
      
    def __init__(self, trace, log, offset_wait, wait, default_wait):            
            self.log = log
            self.offset_wait = offset_wait
            self.wait = wait
            self.default_wait = default_wait
            self.trace = trace
      
    @_error_decorator()
    def wait_human(self, offset=-1, tmp=-1):
        self.trace(inspect.stack())
        loffset = offset
        loffwait = tmp

        if (offset == -1):
                loffset = self.offset_wait
                loffwait = self.wait
        if (tmp == -1):
                loffwait = self.default_wait
        random.random()
        res = random.randint(loffset, loffset+loffwait)
        self.log.lg(f"wait for {res} seconds")
        sleep(res)