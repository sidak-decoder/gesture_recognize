import streamlit as st
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import db
import signupacc
import gestures as gstr

class Login:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.width, self.height = self.login_window.winfo_screenwidth(), self.login_window.winfo_screenheight()
        self.login_window.geometry(f"{self.width}x{self.height}")

        # Load login background image
        self.login_background_image = Image.open("bg.jpg")
        self.login_background_image = self.login_background_image.resize((self.width, self.height), Image.LANCZOS)
        self.login_background_photo = ImageTk.PhotoImage(self.login_background_image)

        # Place login background image on the login window
        self.login_background_label = tk.Label(self.login_window, image=self.login_background_photo)
        self.login_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.namevar = StringVar()
        self.name = Label(self.login_window, text="Username", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.name.place(x=200, y=200, width=160, height=30)
        self.entername = Entry(self.login_window, font=('Verdana', 14), textvariable=self.namevar)
        self.entername.place(x=370, y=200, width=230, height=30)

        self.pwdvar = StringVar()
        self.pwd = Label(self.login_window, text="Password", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.pwd.place(x=200, y=240, width=160, height=30)
        self.enterpwd = Entry(self.login_window, font=('Verdana', 14), show="*", textvariable=self.pwdvar)
        self.enterpwd.place(x=370, y=240, width=230, height=30)

        self.var = IntVar()
        self.checkB = Checkbutton(text='Show Password', font=('Verdana', 12, 'bold'), fg="#20262E", bg="#F5EAEA", variable=self.var, onvalue=1,
                                  offvalue=0, command=self.Showpasswd)
        self.checkB.place(x=370, y=280, width=230, height=30)

        self.signin = Button(self.login_window, text="Login", font=('Verdana', 14, 'bold'), command=self.signinclick)
        self.signin.place(x=200, y=340, width=400, height=30)

        self.signup = Label(self.login_window, text="Don't have an account?", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.signup.place(x=200, y=440, width=400, height=30)
        self.btnsignup = Button(self.login_window, text="Sign Up", font=('Verdana', 14, 'bold'), command=self.signupclick)
        self.btnsignup.place(x=200, y=480, width=400, height=30)

    def Showpasswd(self):
        if (self.var.get()):
            self.enterpwd.config(show="")
        else:
            self.enterpwd.config(show="*")

    def signupclick(self):
        self.login_window.destroy()
        signupacc.signupacc()

    def signinclick(self):
        name = self.namevar.get()
        pwd = self.pwdvar.get()
        if name == "" and pwd == "":
            messagebox.showerror("Admin", "Please enter valid details.")
        else:
            if db.existingAcc(name, pwd):
                messagebox.showinfo("Admin", "Welcome...")
                self.login_window.destroy()
                gstr.gestures()
            else:
                messagebox.showerror("Error", "Invalid Username or Password, Try Again!")

def main():
    login = Login()
    login.login_window.mainloop()

if __name__ == "__main__":
    main()