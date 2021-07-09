from Logger import *
import threading
import datetime
import time
import os
import pyautogui
import hashlib
from win32gui import GetWindowText, GetForegroundWindow
import subprocess

fake_data = {
    'new-version': False,
    'editing': True,
    'parent': '123',
    'child': '456',
    'mon': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'tues': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'thurs': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'sat': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'sun': ['F18:00 T18:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90']
}


def get_parent():
    return fake_data['parent']


def change_pwd(new_pwd, parent=False, child=False):
    if parent == child:
        raise Exception("Can't change both pwd at the same time\n Or not change anything at all")
    else:
        if parent:
            role = 'parent'
        else:
            role = 'child'
        hashed_pwd = hashlib.sha256(new_pwd.encode()).hexdigest()
        fake_data[role] = hashed_pwd

'''
change_pwd('123', parent=True)
print(fake_data)
pwd_input = '123'
hashed_pwd = hashlib.sha256(pwd_input.encode()).hexdigest()
print(fake_data['parent'] == pwd_input)
print(pwd_input)
'''
# Tue Wed Thu Fri Sat Sun Mon
'''
# [next_available(datetime), date_of_this_time_rule, F, T, D, I, S]
logger = Logger()
key_log_thread = threading.Thread(target=logger.begin, daemon=True)
key_log_thread.start()
t1 = time.perf_counter()
sec = 10
while sec > 0:
    print("counting")
    time.sleep(1)
    sec -= 1
print("Complete")
t2 = time.perf_counter()
print(t2 - t1)
'''
'''
test = [ 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90','F06:00 T06:45']
test.sort()
print(test)
'''
last_window = ""
while True:
    active_window = (GetWindowText(GetForegroundWindow()))
    if active_window != last_window:
        last_window = active_window
        now = datetime.datetime.now().strftime('[%H:%M]\n')
        print(now)
        print(active_window)
