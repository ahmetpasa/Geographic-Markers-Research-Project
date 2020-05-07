#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 23:19:34 2020

@author: alibozkurt
"""
from tkinter import *
import os


def delete1():
       
    screen2.destroy()

def delete2():
       
    screen3.destroy()
    
    
def successful_entrance():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Success")
    screen3.geometry("150x100")
    
    Label(screen3, text = "Login Success", fg="green", font = ("Arial", 12)).pack()
    Button(screen3,text="OK", command = delete2).pack()
    
    
def login_check():
    a= username_login.get()
    b = password_login.get()
       
    list_of_files = os.listdir()  
    
    if a in list_of_files:
        file1 = open(a, "r")
        temp = file1.read().splitlines()
        
        if b in temp:
            
            successful_entrance()
        else:
            
            Label(screen2, text="\n\n\n").pack()
            c = Label(screen2, text = "Password Error. Try again...", fg="red", font = ("Arial", 10))
            c.pack()
            
            screen2.after(2000, delete1)
            
    else:
        Label(screen2, text="\n\n\n").pack()
        c = Label(screen2, text = "User Not Found...\n closing...", fg="red", font = ("Arial", 10))
        c.pack()
        screen2.after(2000, delete1)
    

def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    
    l = Label(screen2, text="Login Page", font=("Calibri", 12))
    l.pack()
    Label(screen2, text="").pack()
    
    global username_login
    global password_login
    
    username_login = StringVar()
    password_login = StringVar()
    
    k = Label(screen2, text = "Username * ")
    k.pack()
    
    global username_entry1
    username_entry1 = Entry(screen2, textvariable = username_login)
    username_entry1.pack()
    
    Label(screen2, text = "Password * ").pack()
    
    global password_entry1
    password_entry1 = Entry(screen2, textvariable = password_login, show="*")
    password_entry1.pack()

    Label(screen2, text = "").pack()

    b = Button(screen2, text="Login", width = 10, height =1, command = login_check)
    b.pack() 
    
    
    
def registerOnFile():
    
    a = username.get()
        
    file = open(a, "w")
    file.write(username.get() + "\n")
    file.write(password.get() + "\n")
    file.close()
       
    c = Label(screen1, text = "Registration process is successfully\ncompleted", fg="green", font = ("Arial", 10))
    c.pack()
    
    
def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")
     
    
    global username
    global password
    username = StringVar()
    password = StringVar()
    
    k = Label(screen1, text = "Registration Page", font=("Calibri", 12))
    k.pack()
    Label(screen1, text = "").pack()
   
    
    a = Label(screen1, text = "Username *")
    a.pack()
    
    global username_entry
    username_entry = Entry(screen1, textvariable = username).pack()
        
    b = Label(screen1, text = "Password *")
    b.pack()
   
    global password_entry
    password_entry = Entry(screen1, textvariable = password).pack()
    
    
    Label(screen1, text = "").pack()
    
    Button(screen1, text = "Register", width=10, height=1, command=registerOnFile).pack()  

def main_screen():
    
    global screen
    screen = Tk()
    screen.geometry("600x400")
    screen.title("Main Page")
    
    
    photo2 = PhotoImage(file='login.png')  # it can be put on journal logo etc this image bigger
    photo = Label(screen, image=photo2, bg='white')
    photo.pack()
    
    Label(screen, text = "").pack()
    
    Label(screen, text="Geographic Markers \nResearch Project", bg="grey", height="2", width = "25",  font=("Arial", 11)).pack()
    
  
    Label(screen, text = "\n").pack()
    
    
    Button(screen, text = "Login", height="2", width = "30", command=login).pack()
    
    Label(screen, text = "").pack()
    
    Button(screen, text = "Register" ,height="2", width = "30", command=register).pack()
    
    
    
    screen.mainloop()




main_screen()
