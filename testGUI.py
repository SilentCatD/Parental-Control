
from tkinter import *


window = Tk()
window.title('Child management')
window.rowconfigure(0, minsize=350)
window.columnconfigure([0, 1, 2, 3], minsize=200)
window.geometry("600x450")

#button = Button(window,text = "Parent" , command=lambda: print("Change Parent pass"))
#button2 = Button(window,text = "Child" , command=lambda: print("Change Child pass"))
#button3 = Button(window,text = "Cancel" , command=lambda: cancel_pass())   



def main_menu():
    text1 = "Change password"
    text2 = "Edit"
    button = Button(window,text = text1, command=lambda: changePass(button,button2))
    button2 = Button(window,text = text2 , command=lambda: Edit(button,button2))
    button.grid(row = 1, column = 0)
    button2.grid(row = 1, column = 1)

def cancel_pass(button,button2,button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    main_menu()


def changePass(button,button2):
    button.destroy()
    button2.destroy()
    button = Button(window,text = "Parent" , command=lambda:changeParentPass(button,button2,button3))
    button2 = Button(window,text = "Child" , command=lambda: changeChildPass(button,button2,button3))
    button3 = Button(window,text = "Cancel" , command=lambda: cancel_pass(button,button2,button3)) 
    button.grid(row = 1, column = 0)
    button2.grid(row = 1, column = 1)
    button3.grid(row = 1, column = 2)

def cancel_passParent(label1,entry,button,button2):
    label1.destroy()
    entry.destroy()
    button.destroy()
    button2.destroy()
    changePass(button,button2)

def changeParentPass(button,button2,button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    label1 = Label(text = "Password")
    entry = Entry()
    button = Button(window,text = "Confirm" , command=lambda: print("Confirm"))
    button2 = Button(window,text = "Cancel" , command=lambda: cancel_passParent(label1,entry,button,button2))
    label1.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button.grid(row = 1, column = 0)
    button2.grid(row = 1, column = 1)

def cancel_passChild(label1,entry,button,button2):
    label1.destroy()
    entry.destroy()
    button.destroy()
    button2.destroy()
    changePass(button,button2)

def changeChildPass(button,button2,button3):
    button.destroy()
    button2.destroy()
    button3.destroy()
    label1 = Label(text = "Password")
    entry = Entry()
    button = Button(window,text = "Confirm" , command=lambda: print("Confirm"))
    button2 = Button(window,text = "Cancel" , command=lambda: cancel_passParent(label1,entry,button,button2))
    label1.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button.grid(row = 1, column = 0)
    button2.grid(row = 1, column = 1)

def select():
    my_label.config(text = my_listbox.get(ANCHOR))

def Edit(button,button2):
    button.destroy()
    button2.destroy()
    global my_listbox
    my_listbox = Listbox(window)
    my_listbox.pack(pady = 15)
    my_list = ["mon","tues","thurs","sat","sun"]
    for item in my_list:
        my_listbox.insert(END,item)
    button = Button(window,text = "Select" , command = select )
    button2 = Button(window,text = "Cancel" , command=lambda: print("Cancel"))
    button.pack(pady= 10)
    button2.pack(pady= 10)
    global my_label
    my_label = Label(window,text = '')
    my_label.pack()

def EditEveryDay():
    print("hello")

if __name__ == '__main__':
    main_menu()
    #if(interface == "main"):

        #print(interface)
    #if(interface == "changePass"):
        #interface = changePass()
mainloop()

