import tkinter as tk
import threading
import subprocess
import time
from PasswordManager import PasswordManager
from Logger import Logger
from TimeManager import TimeManager
import os
from DataFileManager import DataFileManager

lock = threading.Lock()


class MainProgram:
    def __init__(self, master):
        self.master = master
        self.label_text = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_text)
        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_text, show="*")
        self.submit_btn = tk.Button(self.master, text="Check result", command=lambda: self.check_pwd(self.entry_text))
        self.input_sec = 15
        self.parent_sec = 3600
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
        self.data_mng = DataFileManager('data.json', 'key.key')
        self.create_main_window()
        self.data = self.data_mng.get_data()
        self.data_mng.switch_need_update(False)

    def shutdown(self):
        self.data_mng.switch_writing(False)
        self.data_mng.switch_editing(False)
        subprocess.run('echo shut down', shell=True)
        # subprocess.run('shutdown /s /t 1', shell=True)

    def create_main_window(self):
        self.master.title("Parental Control")
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        positionRight = int(self.master.winfo_screenwidth() / 2 - windowWidth / 2) - 200
        positionDown = int(self.master.winfo_screenheight() / 2 - windowHeight / 2) - 200
        self.master.geometry(f'600x450+{positionRight}+{positionDown}')
        self.master.resizable(0, 0)
        self.master.protocol("WM_DELETE_WINDOW", self.disable_event)

    def popup(self, text):
        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        win_x = root_x + 150
        win_y = root_y + 150
        win = tk.Toplevel()
        win.geometry(f'300x50+{win_x}+{win_y}')
        win.wm_title("Notification")
        win.resizable(False, False)
        notification = tk.Label(win, text=text)
        button_close = tk.Button(win, text='OK', command=win.destroy)
        notification.pack()
        button_close.pack()

    def disable_event(self):
        if self.isParent:
            self.data_mng.switch_writing(False)
            self.data_mng.switch_editing(False)
            os._exit(0)
        else:
            self.popup("Only Parent can exit this program")

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
            if self.data_mng.need_update():
                self.label_text.set("New version detected! updating...")
                time.sleep(1)
                logger.end()
                return None
            self.label_text.set(self.tm.get_use_time())
            time.sleep(1)
            sec -= 1
            if sec == 0:
                sec = 60
                self.tm.update_curr_time_rule()
        self.label_text.set("Using time is over! Shutting down in 1 minute...")
        time.sleep(60)
        logger.end()
        self.shutdown()

    def changeParentPass(self):
        label1 = tk.Label(text="Password")
        entry1 = tk.Entry()
        button1 = tk.Button(self.master, text="Confirm", command=lambda: [self.data_mng.switch_writing(True),
                                                                          self.pwd_mng.change_pwd(entry1.get(),
                                                                                                  parent=True),
                                                                          self.data_mng.switch_writing(False),
                                                                          self.popup("Parent Password Changed!"),
                                                                          self.data_mng.switch_need_update(True)])
        button2 = tk.Button(self.master, text="Cancel",
                            command=lambda: [label1.place_forget(), entry1.place_forget(), button1.place_forget(),
                                             button2.place_forget(), self.changePass()])
        label1.place(x=210, y=200)
        entry1.place(x=270, y=200)
        button1.place(x=210, y=300)
        button2.place(x=350, y=300)

    def changeChildPass(self):
        label1 = tk.Label(text="Password")
        entry1 = tk.Entry()
        button1 = tk.Button(self.master, text="Confirm", command=lambda: [self.data_mng.switch_writing(True),
                                                                          self.pwd_mng.change_pwd(entry1.get(),
                                                                                                  child=True),
                                                                          self.data_mng.switch_writing(False),
                                                                          self.popup("Child Password Changed!"),
                                                                          self.data_mng.switch_need_update(True)])
        button2 = tk.Button(self.master, text="Cancel",
                            command=lambda: [label1.place_forget(), entry1.place_forget(), button1.place_forget(),
                                             button2.place_forget(), self.changePass()])
        label1.place(x=210, y=200)
        entry1.place(x=270, y=200)
        button1.place(x=210, y=300)
        button2.place(x=350, y=300)

    def changePass(self):
        button1 = tk.Button(self.master, text="Parent",
                            command=lambda: [button1.place_forget(), button2.place_forget(), button3.place_forget(),
                                             self.changeParentPass()])
        button2 = tk.Button(self.master, text="Child",
                            command=lambda: [button1.place_forget(), button2.place_forget(), button3.place_forget(),
                                             self.changeChildPass()])
        button3 = tk.Button(self.master, text="Cancel",
                            command=lambda: [button1.place_forget(), button2.place_forget(), button3.place_forget(),
                                             self.main_menu()])
        button1.place(x=200, y=200)
        button2.place(x=275, y=200)
        button3.place(x=350, y=200)

    # edit
    def cancel_add(self, selectDay):
        my_listbox = tk.Listbox(self.master, width=45)
        my_listbox.place(x=180, y=0)
        for item in self.data[selectDay]:
            my_listbox.insert(tk.END, item)
        button1 = tk.Button(self.master, text="Add",
                            command=lambda: [button1.place_forget(), button2.place_forget(), button3.place_forget(),
                                             self.add(my_listbox, selectDay)])
        button2 = tk.Button(self.master, text="Delete", command=lambda: self.deleteTime(my_listbox, selectDay))
        button3 = tk.Button(self.master, text="Cancel",
                            command=lambda: [my_listbox.place_forget(), button1.place_forget(), button2.place_forget(),
                                             button3.place_forget(), self.Edit()])
        button1.place(x=200, y=200)
        button2.place(x=275, y=200)
        button3.place(x=350, y=200)

    def addTime(self, my_listbox, selectDay, entry1, entry2, entry3, entry4, entry5):
        string = ""
        if entry1.get() != "":
            string += "F" + entry1.get() + " "
        if entry2.get() != "":
            string += "T" + entry2.get() + " "
        if entry3.get() != "":
            string += "D" + entry3.get() + " "
        if entry4.get() != "":
            string += "I" + entry4.get() + " "
        if entry5.get() != "":
            string += "S" + entry5.get()
        if string != "":
            # to DO
            self.data[selectDay].append(string)
            self.data[selectDay].sort()
            # ------------------
            self.data_mng.switch_writing(True)
            self.data_mng.save_data(self.data)
            self.data_mng.switch_writing(False)
            self.data_mng.switch_need_update(True)
            my_listbox.insert(tk.END, string)

    def add(self, my_listbox, selectDay):
        label1 = tk.Label(text="From")
        label2 = tk.Label(text="To")
        label3 = tk.Label(text="Duration")
        label4 = tk.Label(text="interrupt")
        label5 = tk.Label(text="sum")
        entry1 = tk.Entry()
        entry2 = tk.Entry()
        entry3 = tk.Entry()
        entry4 = tk.Entry()
        entry5 = tk.Entry()
        my_listbox.place(x=180, y=0)
        label1.place(x=180, y=200)
        entry1.place(x=240, y=200)
        label2.place(x=180, y=225)
        entry2.place(x=240, y=225)
        label3.place(x=180, y=250)
        entry3.place(x=240, y=250)
        label4.place(x=180, y=275)
        entry4.place(x=240, y=275)
        label5.place(x=180, y=300)
        entry5.place(x=240, y=300)
        button = tk.Button(self.master, text="Add",
                           command=lambda: self.addTime(my_listbox, selectDay, entry1, entry2, entry3, entry4, entry5))
        button2 = tk.Button(self.master, text="Cancel", command=lambda: [
            my_listbox.place_forget(),
            label1.place_forget(),
            label2.place_forget(),
            label3.place_forget(),
            label4.place_forget(),
            label5.place_forget(),
            entry1.place_forget(),
            entry2.place_forget(),
            entry3.place_forget(),
            entry4.place_forget(),
            entry5.place_forget(),
            button.place_forget(),
            button2.place_forget(),
            self.cancel_add(selectDay)])
        button.place(x=250, y=325)
        button2.place(x=300, y=325)

    def deleteTime(self, my_listbox, selectDay):
        selectDel = my_listbox.get(tk.ANCHOR)
        if selectDel != "":
            my_listbox.delete(tk.ANCHOR)
            self.data[selectDay].remove(selectDel)
            # ---------------------------
            self.data_mng.save_data(self.data)
            self.data_mng.switch_need_update(True)

    def select_menu(self, selectDay):
        if selectDay == "":
            return self.Edit()
        my_listbox = tk.Listbox(self.master, width=45)
        my_listbox.place(x=180, y=0)
        for item in self.data[selectDay]:
            my_listbox.insert(tk.END, item)
        button1 = tk.Button(self.master, text="Add",
                            command=lambda: [button1.place_forget(), button2.place_forget(), button3.place_forget(),
                                             self.add(my_listbox, selectDay)])
        button2 = tk.Button(self.master, text="Delete", command=lambda: self.deleteTime(my_listbox, selectDay))
        button3 = tk.Button(self.master, text="Cancel",
                            command=lambda: [my_listbox.place_forget(), button1.place_forget(), button2.place_forget(),
                                             button3.place_forget(), self.Edit()])
        button1.place(x=200, y=200)
        button2.place(x=275, y=200)
        button3.place(x=350, y=200)

    def Edit(self):
        self.data = self.data_mng.get_data()
        self.data_mng.switch_editing(True)
        my_listbox = tk.Listbox(self.master)
        my_listbox.place(x=225, y=0)
        my_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for item in my_list:
            my_listbox.insert(tk.END, item)
        button = tk.Button(self.master, text="Select",
                           command=lambda: [self.select_menu(selectDay=my_listbox.get(tk.ANCHOR)),
                                            button.place_forget(), button2.place_forget(),
                                            my_listbox.place_forget()])
        button2 = tk.Button(self.master, text="Cancel",
                            command=lambda: [my_listbox.place_forget(), button.place_forget(),
                                             button2.place_forget(), self.main_menu(),
                                             self.data_mng.switch_editing(False)])
        button.place(x=210, y=200)
        button2.place(x=300, y=200)

    def main_menu(self):
        button1 = tk.Button(self.master, text="Change password",
                            command=lambda: [button1.place_forget(), button2.place_forget(), self.changePass()])
        button2 = tk.Button(self.master, text="Edit",
                            command=lambda: [button1.place_forget(), button2.place_forget(),
                                             self.Edit(), self.data_mng.switch_editing(True)])
        button1.place(x=210, y=350)
        button2.place(x=350, y=350)

    def parent_gui(self):
        self.main_menu()

    def clear_widgets(self):
        for widgets in self.master.winfo_children():
            widgets.forget()

    def logic(self):
        if self.tm.in_penalty():
            print("in penalty")
            self.label_text.set(f'In penalty time, shutting down...\nCome back after {self.tm.get_penalty()}')
            self.label.pack()
            lock.acquire()
            time.sleep(5)
            lock.release()
            self.shutdown()
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
                    self.shutdown()

            else:
                self.current_attempt = 0
                if self.isParent:
                    self.label_text.set("Logged in as Parent!")
                    self.entry.forget()
                    self.submit_btn.forget()
                    self.parent_gui()
                    self.count_parent()
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
                    time.sleep(2)
                    lock.release()
                    self.count_children()
                    if self.data_mng.need_update():
                        self.data_mng.switch_need_update(False)
                        self.data = self.data_mng.get_data()
                        self.pwd_mng.update_data()
                        self.tm.update_data()
                        self.tm.curr_time_rule_reset()

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
