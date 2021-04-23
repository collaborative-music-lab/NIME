import time 

######################
#CONFIGURE TIMEOUT
######################
#number of minutes after which python script will automatically
#cancel itself if it hasn't received an OSC message


#you can also cancel the script by calling t.cancel()
# sending an OSC "/cancel" message

class Timeout: 
    _interval = 5
    _unit = 60 # timeout = (interval*unit) seconds
    _counter = 0
    _cancel = 0
    
    def __init__(self,interval):
      """ Sets the timeout period"""
      _interval = interval

    def check(self):
        if time.perf_counter() - self._counter > self._interval * self._unit:
            #cancel this script
            print("cancelled script")
            return 0
        if self._cancel == 1:
            print("cancelled script")
            return 0
        return 1

    def update(self):
        self._counter = time.perf_counter()

    def cancel(self):
        self._cancel = 1