import Tkinter
import tkMessageBox
from Tkinter import *
from socket import AF_INET, SOCK_STREAM, socket

root = Tk()

def updateData():
   tkMessageBox.showinfo( "Alert", "your update code should be here")

def commitData():
   s = socket(AF_INET, SOCK_STREAM)
   server_address = ('127.0.0.1', 7777)
   s.connect(server_address)

   message = T.get("1.0",END)

   if s.sendall(message) == None:
      print 'Success'
      s.close()
   else:
      print 'Error'

B1 = Tkinter.Button(root, text ="Update", command = updateData)
B1.grid(row=0, column=0)

B2 = Tkinter.Button(root, text ="Commit", command = commitData)
B2.grid(row=0, column=1)

T = Text(root, height=20, width=100)
T.grid(row=1, column=0, columnspan=2)

root.title('Client3')
root.minsize(width=600, height=400)
mainloop()

