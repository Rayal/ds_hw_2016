import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def updateData():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

def commitData():
   tkMessageBox.showinfo( "aaaaa", "bbbbb")

B1 = Tkinter.Button(top, text ="Update", command = updateData)
B1.grid(row=0, column=0)


B2 = Tkinter.Button(top, text ="Commit", command = commitData)
B2.grid(row=0, column=1)

L1= Tkinter.en
top.mainloop()

