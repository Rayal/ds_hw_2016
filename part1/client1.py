import Tkinter
import tkMessageBox
from Tkinter import *
from tcp.mboard.sessions.client.protocol import edit_file, request_file


root = Tk()

server_address = ('127.0.0.1', 7777)

def pulldata(self):
    updated_text= request_file(server_address, T_filename.get("1.0", END))
    T_text.insert(END, updated_text)

def pushdata():
    file_name = T_filename.get()
    txt_body = T_text.get("1.0", END)
    edit_file(server_address,file_name,txt_body)

btn_pull = Tkinter.Button(root, text ="Pull", width=10, command = pulldata)
btn_pull.grid(row=0, column=0)

btn_push = Tkinter.Button(root, text ="Push", width=10, command = pushdata)
btn_push.grid(row=0, column=1)

lbl_1 = Label(root, text="File Name")
lbl_1.grid(row=1, column=0)

T_filename = Entry(root, width=30)
T_filename.grid(row=1, column=1)

T_text = Text(root, height=20, width=100)
T_text.grid(row=4, column=0, columnspan=2)

root.title('Client1')
root.minsize(width=600, height=400)
mainloop()

