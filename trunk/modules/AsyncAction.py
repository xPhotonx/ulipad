import Queue
import threading, thread
import time
import Globals

class AsyncAction(threading.Thread):
    def __init__(self, timestep=.1, interval=0.05):
        super(AsyncAction, self).__init__()
        self.q = Queue.Queue(0)
        self.setDaemon(True)
        self.lock = thread.allocate_lock()
        self.stop = False
        self.running = False
        self.timestep = timestep
        self.last = None
        self.interval = interval
        
    def put(self, obj):
        self.q.put((obj, time.time()))
        
    def stop(self):
        self.stop = True
        
    def _empty(self):
        return self.q.empty()
    empty = property(_empty)
    
    def clear(self):
        self.lock.acquire()
        while 1:
            try:
                obj = self.q.get_nowait()
            except:
                break
        self.lock.release()
        
    def run(self):
        try:
            while not self.stop:
                if Globals.app.wxApp.Active and not self.q.empty() and not self.running:
                    self.lock.acquire()
                    while 1:
                        try:
                            obj = self.q.get_nowait()
                            if obj:
                                self.last = obj
                        except:
                            break
                    self.lock.release()
                if self.last:
                    if not self.running:
                        if time.time() - self.last[1] < self.timestep:
                            continue
                        self.running = True
                        try:
                            self.do_action(self.last[0])
                            self.last = None
                        except:
#                            import traceback
#                            traceback.print_exc()
                            pass
                        self.running = False
                time.sleep(self.interval)
        except:
            pass
            
    def do_action(self, obj):
        '''
        you should judge if not self.empty to quit the process, because
        it means that there is proceed infos need to process, so current
        one should ba cancelled
        '''
        pass
    
if __name__ == '__main__':
    class Test(AsyncAction):
        def do_action(self, obj):
            time.sleep(0.5)
            if not self.empty:
                print 'xxxxxxxxxxxxxxxx', obj
                return
            print 'pppppp', obj
            
    a = Test(1)
    a.start()
    for i in range(100):
        a.put(i)
        print 'put', i
        time.sleep(.1)
    time.sleep(10)