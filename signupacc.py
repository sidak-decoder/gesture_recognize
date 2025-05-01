import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import db
from login import *

class signupacc:
    def Showpasswd(self):
            if (self.var.get()):
                self.enterpwd.config(show="")
            else:
                self.enterpwd.config(show="*")

    def validate_email(self, email):
        # Simple regex for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        # Ensure phone number is at least 10 digits
        return phone.isdigit() and len(phone) == 10

    def clicksignup(self):
        name=self.namevar.get()
        email=self.emailvar.get()
        phone=self.phonevar.get()
        gender=self.genvar.get()
        pwd=self.pwdvar.get()

        if not name or not email or not phone or not pwd:
            messagebox.showerror("Admin", "Please enter all details.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Admin", "Please enter a valid email address.")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Admin", "Please enter a valid phone number (10 digits).")
            return

        #create new file for database so that we can fetch these values in database and install mysql.connector lib(pipi install mysql.connector)
        #we create a db file as db.py
        if name=="" and email=="" and phone=="" and pwd=="" :
            messagebox.showerror("Admin","Please enter valid details.")
        else:
            data=(name,email,phone,gender,pwd)
            if db.insertregister(data):  #if this is true
                messagebox.showinfo("Admin","Account created")
                self.namevar.set("")   #to clear textfield after submitting details then we enter first in textfields
                self.pwdvar.set("")
                self.emailvar.set("")
                self.phonevar.set("")
                self.signup_window.destroy()
                login()
            else:
                messagebox.showerror("Admin","Something went wrong")
    
    def __init__(self):
        self.signup_window = tk.Tk()
        self.signup_window.title("Sign Up")
        self.width, self.height = self.signup_window.winfo_screenwidth(), self.signup_window.winfo_screenheight()
        self.signup_window.geometry(f"{self.width}x{self.height}")

        # Load login background image
        self.login_background_image = Image.open("bg.jpg")
        self.login_background_image = self.login_background_image.resize((self.width, self.height), Image.LANCZOS)
        self.login_background_photo = ImageTk.PhotoImage(self.login_background_image)

        # Place login background image on the login window
        self.login_background_label = tk.Label(self.signup_window, image=self.login_background_photo)
        self.login_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.namevar=StringVar()
        self.name=Label(self.signup_window, text="Username", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.name.place(x=200,y=200,width=160,height=30)
        self.entername=Entry(self.signup_window, font=('Verdana', 14),textvariable=self.namevar)
        self.entername.place(x=370,y=200,width=230,height=30)

        self.emailvar=StringVar()
        self.email=Label(self.signup_window, text="Email", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.email.place(x=200,y=240,width=160,height=30)
        self.enteremail=Entry(self.signup_window, font=('Verdana', 14),textvariable=self.emailvar)
        self.enteremail.place(x=370,y=240,width=230,height=30)

        self.phonevar=StringVar()
        self.phone=Label(self.signup_window, text="Phone No.", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.phone.place(x=200,y=280,width=160,height=30)
        self.enterphone=Entry(self.signup_window, font=('Verdana', 14),textvariable=self.phonevar)
        self.enterphone.place(x=370,y=280,width=230,height=30)

        self.gender=Label(self.signup_window, text="Gender", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.gender.place(x=200,y=320,width=160,height=30)
        self.genvar=IntVar()
        self.male=Radiobutton(self.signup_window,value="1",text="Male",variable=self.genvar,font=('Verdana', 14, 'bold'), fg="#20262E", bg="#F5EAEA")
        self.male.place(x=370,y=320,width=100,height=30)
        self.female=Radiobutton(self.signup_window,value="2",text="Female",variable=self.genvar,font=('Verdana', 14, 'bold'), fg="#20262E", bg="#F5EAEA")
        self.female.place(x=490,y=320,width=110,height=30)

        self.pwdvar=StringVar()
        self.pwd=Label(self.signup_window, text="Password", font=('Verdana', 14, 'bold'), bg="#20262E", fg="#F5EAEA")
        self.pwd.place(x=200,y=360,width=160,height=30)
        self.enterpwd=Entry(self.signup_window, font=('Verdana', 14), show="*",textvariable=self.pwdvar)  
        self.enterpwd.place(x=370,y=360,width=230,height=30)

        self.var = IntVar()
        self.checkB = Checkbutton(text='Show Password', font=('Verdana', 12, 'bold'), 
                                  fg="#20262E", bg="#F5EAEA", variable=self.var, onvalue=1,
                                  offvalue=0, command=self.Showpasswd)
        self.checkB.place(x=370,y=400,width=230,height=30)

        self.btnsignup=Button(self.signup_window, text="Sign Up", font=('Verdana', 14, 'bold'), fg="#20262E", bg="#F5EAEA", command=self.clicksignup)   
        self.btnsignup.place(x=200,y=480,width=400,height=30)

        self.signup_window.mainloop()
        
if __name__ == "__main__":
    s=signupacc()