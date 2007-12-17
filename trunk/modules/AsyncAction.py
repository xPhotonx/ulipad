import Queue
import threading, thread
import time
import Globals

class AsyncAction(threading.Thread):
    def __init__(self, timestep=.1):
        super(AsyncAction, self).__init__()
        self.q = Queue.Queue(0)
        self.setDaemon(True)
        self.lock = thread.allocate_lock()
        self.stop = False
        self.step = timestep
        self.running = False
        
    def put(self, obj):
        self.q.put(obj)
        
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
                    last = None
                    while 1:
                        try:
                            obj = self.q.get_nowait()
                            last = obj
                        except:
                            break
                    self.lock.release()
                    if last:
                        if not self.running:
                            self.running = True
                            try:
                                self.do_action(last)
                            except:
                                pass
                            self.running = False
                time.sleep(self.step)
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