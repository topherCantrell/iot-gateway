import tkinter

root = tkinter.Tk()
root.configure(background='black')
root.attributes('-fullscreen', True)

status = tkinter.Label(root, text='-10.4F', bg='green', fg='black', width=20, height=5)
status.place(x=100, y=100)

root.mainloop()
