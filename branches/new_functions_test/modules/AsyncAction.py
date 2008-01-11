import Queue
import threading
import time
from modules import Globals
KEYS = [' ','=','/','[']
class AsyncAction(threading.Thread):
    def __init__(self, timestep=.1):
        super(AsyncAction, self).__init__()
        self.q = Queue.Queue(0)
        self.setDaemon(True)
        self.stop = False
        self.timestep = timestep
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
                self.prev = 1000
                obj = None
                while 1:
                    try:
                        if  self.timestep == "InputAssistantAction":
                            obj = self.q.get(True, float(Globals.mainframe.pref.inputass_typing_rate)/1000)
                            if obj['on_char_flag']:
                                tt = obj['event'].time_stamp - self.prev < Globals.mainframe.pref.inputass_typing_rate
                                self.prev = obj['event'].time_stamp
                                key = obj['event'].GetKeyCode()
                                if chr(key) in KEYS and tt:
                                    self.last = obj
                                    break
                                elif chr(key) in KEYS and (not tt):
                                    try:
                                        obj1 = self.q.get(True, float(Globals.mainframe.pref.inputass_typing_rate*3)/1000)
                                        self.last = obj1
                                    except:
                                        self.last = obj
                                        if self.last:
                                            break
                        else:
                            obj = self.q.get(True, self.timestep)
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