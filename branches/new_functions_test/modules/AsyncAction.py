import Queue
import threading
import time
class AsyncAction(threading.Thread):
    def __init__(self):
        super(AsyncAction, self).__init__()
        self.q = Queue.Queue(0)
        self.setDaemon(True)
        self.stop = False
        self.last = None
        
    def put(self, obj):
        self.q.put(obj)
        
    def stop(self):
        self.stop = True
        
    def _empty(self):
        return self.q.empty()
    empty = property(_empty)
    
    def clear(self):
        while 1:
            try:
                obj = self.q.get_nowait()
            except:
                break
        
    def run(self):
        try:
            while not self.stop:
                self.last = None
                while 1:
                    try:
                        obj = self.q.get(True, self.do_timeout())
                        self.last = obj
                    except:
                        if self.last:
                            break

                if self.last:
                    try:
                        self.do_action(self.last)
                        self.last = None
                    except:
                        pass

        except:
            pass
        
    def do_timeout(self):
        '''
        if you want to change thread timeout value,overwrite this method.
        
        '''        
        return 0.1
    
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
            
    a = Test()
    a.start()
    for i in range(100):
        a.put(i)
        print 'put', i
        time.sleep(.1)
    time.sleep(10)