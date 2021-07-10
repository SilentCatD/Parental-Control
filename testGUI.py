from tkinter import *
import tkinter as tk

fake_data = {
    'new-version': False,
    'editing': True,
    'parent': '123',
    'child': '456',
    'mon': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'tues': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'wed': [],
    'thurs': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'fri': [],
    'sat': ['F06:00 T06:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90'],
    'sun': ['F18:00 T18:45', 'F07:30 T11:30 D60 I20 S150', 'F19:00 T21:30 S90']
}

window = Tk()
window.title('Child management')
window.rowconfigure(0, minsize=350)
window.columnconfigure([0, 1, 2, 3], minsize=200)
# window.geometry("600x450")
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2) - 200
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2) - 200
window.geometry(f'600x450+{positionRight}+{positionDown}')


# button = Button(window,text = "Parent" , command=lambda: print("Change Parent pass"))
# button2 = Button(window,text = "Child" , command=lambda: print("Change Child pass"))
# button3 = Button(window,text = "Cancel" , command=lambda: cancel_pass())


def main_menu():
    text1 = "Change password"
    text2 = "Edit"
    button = Button(window, text=text1, command=lambda: changePass(button, button2))
    button2 = Button(window, text=text2, command=lambda: Edit(button, button2))
    button.place(x=150, y=400)
    button2.place(x=350, y=400)


def cancel_pass(button, button2, button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    main_menu()


def changePass(button, button2):
    button.destroy()
    button2.destroy()
    button = Button(window, text="Parent", command=lambda: changeParentPass(button, button2, button3))
    button2 = Button(window, text="Child", command=lambda: changeChildPass(button, button2, button3))
    button3 = Button(window, text="Cancel", command=lambda: cancel_pass(button, button2, button3))
    button.place(x=150, y=400)
    button2.place(x=250, y=400)
    button3.place(x=350, y=400)


def cancel_passParent(label1, entry, button, button2):
    label1.destroy()
    entry.destroy()
    button.destroy()
    button2.destroy()
    changePass(button, button2)


def changeParentPass(button, button2, button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    label1 = Label(text="Password")
    entry = Entry()
    button = Button(window, text="Confirm", command=lambda: print("Confirm"))
    button2 = Button(window, text="Cancel", command=lambda: cancel_passParent(label1, entry, button, button2))
    label1.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button.grid(row=1, column=0)
    button2.grid(row=1, column=1)


def cancel_passChild(label1, entry, button, button2):
    label1.destroy()
    entry.destroy()
    button.destroy()
    button2.destroy()
    changePass(button, button2)


def changeChildPass(button, button2, button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    label1 = Label(text="Password")
    entry = Entry()
    button = Button(window, text="Confirm", command=lambda: print("Confirm"))
    button2 = Button(window, text="Cancel", command=lambda: cancel_passParent(label1, entry, button, button2))
    label1.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button.grid(row=1, column=0)
    button2.grid(row=1, column=1)


def deleteTime(my_listbox, selectDay):
    selectDel = my_listbox.get(ANCHOR)
    my_listbox.delete(ANCHOR)
    # fake_data[selectDay].remove(selectDel)
    print("Del" + selectDel)


def addTime(my_listbox, selectDay):
    str = ""
    if entry1.get() != "":
        str += "F" + entry1.get() + " "
    if entry2.get() != "":
        str += "T" + entry2.get() + " "
    if entry3.get() != "":
        str += "D" + entry3.get() + " "
    if entry4.get() != "":
        str += "I" + entry4.get() + " "
    if entry5.get() != "":
        str += "S" + entry5.get()
    if str != "":
        fake_data[selectDay].append(str)
        fake_data[selectDay].sort()
        my_listbox.insert(END, str)


def add(my_listbox, selectDay, button, button2, button3):
    my_listbox.forget()
    button.destroy()
    button2.destroy()
    button3.destroy()
    global label1, label2, label3, label4, label5
    label1 = Label(text="From")
    label2 = Label(text="To")
    label3 = Label(text="Duration")
    label4 = Label(text="interrupt")
    label5 = Label(text="sum")
    global entry1, entry2, entry3, entry4, entry5
    entry1 = Entry()
    entry2 = Entry()
    entry3 = Entry()
    entry4 = Entry()
    entry5 = Entry()
    window.rowconfigure(0, minsize=50)
    window.columnconfigure([0, 1, 2, 3, 4], minsize=50)
    my_listbox.grid(row=0, column=1)
    label1.grid(row=1, column=0)
    entry1.grid(row=1, column=1)
    label2.grid(row=2, column=0)
    entry2.grid(row=2, column=1)
    label3.grid(row=3, column=0)
    entry3.grid(row=3, column=1)
    label4.grid(row=4, column=0)
    entry4.grid(row=4, column=1)
    label5.grid(row=5, column=0)
    entry5.grid(row=5, column=1)
    button = Button(window, text="Add", command=lambda: addTime(my_listbox, selectDay))
    button2 = Button(window, text="Cancel", command=lambda: cancel_add(my_listbox, button, button2, selectDay))
    button.grid(row=3, column=2)
    button2.grid(row=3, column=4)


def cancel_add(my_listbox, button, button2, selectDay):
    label1.destroy()
    label2.destroy()
    label3.destroy()
    label4.destroy()
    label5.destroy()
    entry1.destroy()
    entry2.destroy()
    entry3.destroy()
    entry4.destroy()
    entry5.destroy()
    button.destroy()
    button2.destroy()
    my_listbox.destroy()
    my_listbox = Listbox(window, width=45)
    my_listbox.pack(pady=15)
    for item in fake_data[selectDay]:
        my_listbox.insert(END, item)
    button.forget()
    button2.forget()
    button = Button(window, text="Add", command=lambda: add(my_listbox, selectDay, button, button2, button3))
    button2 = Button(window, text="Delete", command=lambda: deleteTime(my_listbox, selectDay))
    button3 = Button(window, text="Cancel", command=lambda: cancel_select(my_listbox, button, button2, button3))
    button.pack(pady=15)
    button2.pack(pady=15)
    button3.pack(pady=15)


def cancel_select(my_listbox, button, button2, button3):
    my_listbox.destroy()
    button.destroy()
    button2.destroy()
    button3.destroy()
    Edit(button, button2)


def select(my_listbox, button, button2):
    selectDay = my_listbox.get(ANCHOR)
    if selectDay == "":
        return
    my_listbox.destroy()
    button.destroy()
    button2.destroy()
    my_listbox = Listbox(window, width=45)
    my_listbox.pack(pady=15)
    for item in fake_data[selectDay]:
        my_listbox.insert(END, item)
    button = Button(window, text="Add", command=lambda: add(my_listbox, selectDay, button, button2, button3))
    button2 = Button(window, text="Delete", command=lambda: deleteTime(my_listbox, selectDay))
    button3 = Button(window, text="Cancel", command=lambda: cancel_select(my_listbox, button, button2, button3))
    button.pack(pady=15)
    button2.pack(pady=15)
    button3.pack(pady=15)


def cancel_edit(my_listbox, button, button2):
    my_listbox.destroy()
    button.destroy()
    button2.destroy()
    main_menu()


def Edit(button, button2):
    button.destroy()
    button2.destroy()
    global my_listbox
    my_listbox = Listbox(window)
    my_listbox.pack(pady=15)
    my_list = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
    for item in my_list:
        my_listbox.insert(END, item)
    button = Button(window, text="Select", command=lambda: select(my_listbox, button, button2))
    button2 = Button(window, text="Cancel", command=lambda: cancel_edit(my_listbox, button, button2))
    button.pack(pady=10)
    button2.pack(pady=10)


def EditEveryDay():
    print("hello")


if __name__ == '__main__':
    main_menu()
mainloop()
