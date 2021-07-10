import tkinter as tk
import threading
import subprocess
import time
from PasswordManager import PasswordManager
from Logger import Logger
from TimeManager import TimeManager

lock = threading.Lock()


def shutdown():
    subprocess.run('echo shut down', shell=True)
    # subprocess.run('shutdown /s /t 1', shell=True)


class MainProgram:
    def __init__(self, master):
        self.master = master
        self.master.title("Parental Control")
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        positionRight = int(self.master.winfo_screenwidth() / 2 - windowWidth / 2) - 200
        positionDown = int(self.master.winfo_screenheight() / 2 - windowHeight / 2) - 200
        self.master.geometry(f'600x450+{positionRight}+{positionDown}')
        self.master.resizable(0, 0)
        self.master.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.label_text = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_text)
        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_text)
        self.submit_btn = tk.Button(self.master, text="Check result", command=lambda: self.check_pwd(self.entry_text))
        self.input_sec = 15
        self.parent_sec = 10
        self.pwd_submitted = False
        self.pwd_correct = False
        self.isParent = False
        self.isChild = False
        self.isCounting = False
        self.max_attempts = 3
        self.current_attempt = 0
        self.in_use_time = False
        self.pwd_mng = PasswordManager('data.json', 'key.key')
        self.tm = TimeManager('data.json', 'key.key')

    def disable_event(self):
        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        win_x = root_x + 150
        win_y = root_y + 150
        win = tk.Toplevel()
        win.geometry(f'300x50+{win_x}+{win_y}')
        win.wm_title("Notification")
        win.resizable(False, False)
        l = tk.Label(win, text="Can't exit this program")
        button_close = tk.Button(win, text='OK', command=win.destroy)
        l.pack()
        button_close.pack()

    def get_pwd(self):
        self.label.pack()
        self.entry.pack()
        self.submit_btn.pack()

    def count_input(self):
        lock.acquire()
        temp = self.input_sec
        self.isCounting = True
        lock.release()
        while self.input_sec >= 0 and not self.pwd_correct and self.current_attempt != self.max_attempts:
            print(self.input_sec)
            time.sleep(1)
            lock.acquire()
            self.input_sec -= 1
            lock.release()
        lock.acquire()
        self.input_sec = temp
        self.isCounting = False
        lock.release()

    def count_parent(self):
        lock.acquire()
        temp = self.parent_sec
        self.isCounting = True
        lock.release()
        while self.parent_sec >= 0:
            print(self.parent_sec)
            time.sleep(1)
            lock.acquire()
            self.parent_sec -= 1
            lock.release()
        lock.acquire()
        self.parent_sec = temp
        self.isParent = False
        self.isCounting = False
        self.pwd_correct = False
        lock.release()

    def count_children(self):
        # call keylogger here
        logger = Logger()
        logger.begin()
        sec = 60
        while self.tm.in_use_time():
            self.label_text.set(self.tm.get_use_time())
            time.sleep(1)
            sec -= 1
            if sec == 0:
                sec = 60
                self.tm.update_curr_time_rule()
        self.label_text.set("Using time is over! Shutting down in 1 minute...")
        time.sleep(60)

    def parent_gui(self):
        while self.isParent:
            print(self.parent_sec)

    def logic(self):
        if self.tm.in_penalty():
            print("in penalty")
            self.label_text.set(f'In penalty time, shutting down...\nCome back after {self.tm.get_penalty()}')
            self.label.pack()
            lock.acquire()
            time.sleep(5)
            lock.release()
            shutdown()
        while True:
            if not self.pwd_correct:
                if not self.pwd_submitted:
                    self.label_text.set(f'Enter password to check, you have {self.input_sec} left')
                self.get_pwd()
                if not self.isCounting:
                    count_pwd_inp_thread = threading.Thread(target=self.count_input, daemon=True)
                    count_pwd_inp_thread.start()
                if self.pwd_submitted:
                    self.current_attempt += 1
                    self.label_text.set(f'Wrong password! You have {self.max_attempts - self.current_attempt} attempt '
                                        f'left')
                    self.entry.forget()
                    self.submit_btn.forget()
                    lock.acquire()
                    time.sleep(1)
                    lock.release()
                    self.pwd_submitted = False
                if self.input_sec == 0 or self.max_attempts == self.current_attempt:
                    if self.max_attempts == self.current_attempt:
                        self.tm.set_penalty(10)
                    lock.acquire()
                    self.current_attempt = 0
                    lock.release()
                    self.label_text.set("Login failed! Shutting down...")
                    self.entry.forget()
                    self.submit_btn.forget()
                    time.sleep(3)
                    shutdown()

            else:
                self.current_attempt = 0
                if self.isParent:
                    self.label_text.set("Logged in as Parent!")
                    self.entry.forget()
                    self.submit_btn.forget()
                    if not self.isCounting:
                        count_down_thread = threading.Thread(target=self.count_parent, daemon=True)
                        parent_gui = threading.Thread(target=self.parent_gui, daemon=True)
                        parent_gui.start()
                        count_down_thread.start()
                        count_down_thread.join()

                elif not self.tm.in_use_time():
                    self.label_text.set(f'Not yet time to use the machine!\n'
                                        f'{self.tm.cant_use_reason()}')
                    self.entry.forget()
                    self.submit_btn.forget()
                    self.pwd_correct = False
                    lock.acquire()
                    time.sleep(5)
                    lock.release()
                else:
                    self.label_text.set("Logged in as child!")
                    self.entry.forget()
                    self.submit_btn.forget()
                    lock.acquire()
                    time.sleep(3)
                    lock.release()
                    children_thread = threading.Thread(target=self.count_children, daemon=True)
                    children_thread.start()
                    children_thread.join()
                    shutdown()

    def check_pwd(self, inp):
        lock.acquire()
        self.pwd_correct = True
        result = self.pwd_mng.compare_pwd(inp.get())
        if result[0]:
            self.isParent = True
        elif result[1]:
            self.isChild = True
        else:
            self.pwd_correct = False
            self.pwd_submitted = True
        lock.release()
        self.entry.delete(0, 'end')


if __name__ == '__main__':
    root = tk.Tk()
    program = MainProgram(root)
    main_thread = threading.Thread(target=program.logic, daemon=True)
    main_thread.start()
    root.mainloop()
