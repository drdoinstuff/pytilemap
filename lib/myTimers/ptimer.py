class Timer(object):
    def __init__(self, interval):
        #self.time = time.time()
        self.time = 0
        self.elapsed = 0
        
        self.interval = interval
        self.started = interval
    
    def Reset(self):
        #self.time = time.time()
        self.time = 0
        self.elapsed = 0
        
    def Trigger(self):
        self.elapsed = self.interval
        
    def getTimeRun(self):
        return self.time + self.elapsed
        
    def Update(self):
        #now = time.time()
        self.elapsed += 1
        
        if self.elapsed >= self.interval:
            self.time = self.elapsed
            self.elapsed = 0

            return True
        else:
            return False