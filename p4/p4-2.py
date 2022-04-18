# prototype 4-1: user input

from tkinter import *

class Auth(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x1000")
        self.title("Solver")
        self.resizable(0, 0)

    # frames

        self.Frame1 = Frame(self, height=1000, width=1000, bg="#0a9df2")
        self.Frame1.pack()
    
    # labels

        self.lbl_title = Label(self.Frame1, text="Equation Solver", font="arial 16 bold", bg="#0a9df2")
        self.lbl_title.place(x=200, y=30)
        
    # input

        self.ent_username = Entry(self.Frame1)
        self.ent_username.place(x=110, y=103)
        # show stars instead of normal text for the password
        self.ent_password = Entry(self.Frame1, show="*")
        self.ent_password.place(x=110, y=153)

    # buttons

        self.btn_login = Button(self.Frame1, text="Log In") #command=self.login)
        self.btn_login.place(x=150, y=200)
    
if __name__ == "__main__":
    myApp = Auth()
    myApp.mainloop()