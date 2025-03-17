#!/usr/bin/env python3
#
#  wizard_gui_v2.py
#  
#  Copyright 2025 nap0 
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# Little Math Wizard inspired by the "Little Professor" devices made bi TI

# import modules
from tkinter import *
from tkinter import ttk
import random as rd


class Wizard(Tk):
    def __init__(self):
        super().__init__()
        
        # --- settings window --------------
        self.title("Litte Math Wizard")
        self.geometry("520x600")
        self.configure(bg="#C0C000",padx=20,pady=20)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # --- tkinter variables ------------
        self.tkdisplaystr = StringVar() # is linked to the display label
        self.tkdisplaystr.set("")
        
        # --- variables --------------------
        self.operators=("/", "*", "-", "+") # operators to use in math problem
        self.operator="+" # current operator to be used        
        self.a = 0 # two numbers to use in math problem
        self.b = 0        
        self.level=1 # difficulty level 1..4
        self.answerstr = "" # answer given by user
        self.correctanswer = 0 # correct answer
        self.numberofproblemsinseries = 5 # how many problems in one series
        self.problemnumber = 0 # how many problems have been covered in the series
        self.correctanswers = 0 # how many answers were correct in the series
        self.equalsign = chr(0x003D)
        
        # theme to use with ttk
        ttk.Style().theme_use('alt')
                
        # --- ttk styles -------------------
        ttk.Style().configure("TFrame",
            background="#805000",
            foreground="#000000")
        ttk.Style().configure("TLabel",
            font=("FreeSans",14,"bold"),
            background="#805000",
            padding=10,
            foreground="#000000")
        ttk.Style().configure("display.TLabel",
            font=("FreeMono",15,"bold"),
            background="#000000",
            padding=15,
            foreground="#FF0000")
        ttk.Style().configure("TButton",
            font=("FreeSans",14,"bold"),
            background="#C0C000",
            foreground="#000000")

        # --- ttk frame which covers Tk window -------------
        self.framemain=ttk.Frame(self,padding=(30,0,30,0))
        self.framemain.grid(row=0,column=0,sticky="WENS")
        self.framemain.columnconfigure(0, weight=1)
        self.framemain.rowconfigure(0, weight=0)
        self.framemain.rowconfigure(1, weight=0)
        self.framemain.rowconfigure(2, weight=1)
        
        # --- label for title -------------------------------
        self.photoimage = PhotoImage(file="img_title.png")
        self.labeltitel = ttk.Label(self.framemain,
            background = "#805000",
            padding=(0,15,0,15),
            image = self.photoimage,
            anchor = CENTER)
        self.labeltitel.grid(row=0, column=0, sticky="WENS")
        
        # --- label for display ---------------------------
        self.labeldisplay = ttk.Label(self.framemain,
            style="display.TLabel",
            textvariable=self.tkdisplaystr)
        self.labeldisplay.grid(row=1, column=0, sticky="WENS")
        
        # --- frame for keys ---------------------------
        self.framekeys = ttk.Frame(self.framemain,padding=(0,35,0,10))
        self.framekeys.grid(row=2,column=0,sticky="WENS")
        for c in range(4):
            self.framekeys.columnconfigure(c, weight=1)  
        for r in range(4):
            self.framekeys.rowconfigure(r, weight=1)  
            
        # --- define buttons for numbers 1..9 ------------
        for c in range(3):
            for r in range(3):
                buttonnumber = 7 + c - 3 * r
                self.definebutton(str( buttonnumber ),str( buttonnumber ),r,c)
        
        # define buttons for math operators
        specialchars = ( chr(0x00F7), chr(0x2715), chr(0x2212), chr(0x002B) )
        for r in range(4):
            self.definebutton(specialchars[r], self.operators[r], r, 3)          
        
        # SET button
        self.definebutton("SET","set",3,0)
        
        # 0 button
        self.definebutton("0","0",3,1)
        
        # GO button 
        self.definebutton("GO","go",3,2)
        
        # start up text
        self.tkdisplaystr.set( "Little Math Wizard" )
        self.update()
        
        # set level
        self.after( 1200, self.setlevel("") )
        
        
        
        
    # --- Instance Methods ------------------------------------------------------------------
    
    # Create a tk Button object and position it using the grid() method
    def definebutton(self, keytext, cmdtext, r, c):
        b = ttk.Button(self.framekeys,
            text = keytext,
            command=lambda cmdtext=cmdtext: self.key(cmdtext)
            )
        b.grid( row=r, column=c, sticky="WENS", ipady=7, ipadx=8, padx=12, pady=20 )
        

    # generate a number with a given number of digits
    def generateanumber(self,numberofdigits):
        numbers = (1,2,3,4,5,6,7,8,9)
        numberswzero = (0,1,2,3,4,5,6,7,8,9)
        numberstr = str(rd.choice(numbers))
        if numberofdigits > 1:
            for _ in range( numberofdigits - 1 ):
                numberstr += str(rd.choice(numberswzero))
        return(int(numberstr))
   
    
    # generate a new math problem
    def generateproblem(self):
        # clear previous answer
        self.answerstr = ""
        # random choice of a math operator    
        # self.operator = rd.choice( self.operators )
        # number size depends on level
        match self.level:
            case 1|0:
                digita,digitb = 1,1
            case 2:
                digita,digitb = 2,1
            case 3:
                digita,digitb = 2,2
            case 4:
                digita,digitb = 3,2
        # random generate two numbers and correct answer 
        # , chr(0x2715), chr(0x2212), chr(0x002B) 
        match self.operator:
            case "/":
                self.b = self.generateanumber(digitb)
                self.a = self.b * self.generateanumber(digita)
                self.correctanswer = self.a // self.b
                operatorchar = chr(0x00F7)
            case "*":
                self.a = self.generateanumber(digita)
                self.b = self.generateanumber(digitb)
                self.correctanswer = self.a * self.b
                operatorchar = chr(0x2715)
            case "-":
                self.a = self.generateanumber(digita)
                self.b = self.generateanumber(digitb)
                if self.a < self.b:
                    self.a, self.b = self.b, self.a
                self.correctanswer = self.a - self.b
                operatorchar = chr(0x2212)
            case "+":
                self.a = self.generateanumber(digita)
                self.b = self.generateanumber(digitb)
                self.correctanswer = self.a + self.b
                operatorchar = chr(0x002B)
        # the complete expression
        expression = f"{self.problemnumber + 1}/{self.numberofproblemsinseries}:  {self.a} {operatorchar} {self.b} {self.equalsign} "
        # display problem
        self.tkdisplaystr.set( expression )
        
    
    
    # keep track of user input if length of the number that has been input
    # is equal to lenght of correct answer verify answer and give feedback
    # also keep track of number of correct anwers in series
    def evaluateanswer(self, keytxt):        
        self.answerstr += keytxt
        if len( self.answerstr ) == len( str(self.correctanswer)): 
            answer = int( self.answerstr )
            if answer == self.correctanswer:
                self.tkdisplaystr.set(f"{answer} IS CORRECT") 
                self.correctanswers += 1
                self.after(900,self.nextprobleminseries)               
            else:
                self.tkdisplaystr.set(f"{answer} IS INCORRECT")                
                self.after(900,self.displaycorrectanswer)
            
    
    # display correct answer go to next problem in series
    def displaycorrectanswer(self):
        expression = f"{self.a} {self.operator} {self.b} = {self.correctanswer}"
        self.tkdisplaystr.set(expression)
        self.after(2000,self.nextprobleminseries)
        
    
    # change difficulty level and start new series    
    def setlevel(self,keytxt):
        if (self.level == 0) and keytxt.isnumeric():
            levelinput = int(keytxt)
            if 0 < levelinput < 5:
                self.level = levelinput
            else:
                self.level = 1
            self.tkdisplaystr.set(f"LEVEL IS {self.level}")    
            self.after(800,self.nextprobleminseries)    
        else:
            self.tkdisplaystr.set("LEVEL 1-4?")
            self.level = 0
            self.problemnumber = 0
            self.correctanswers = 0
            
          
    # choose different math operation
    # restart new series of math problems        
    def setoperator(self,keytxt):
        if keytxt in self.operators:
            self.operator = keytxt
            match self.operator:
                case"+":
                    self.tkdisplaystr.set("Additions")
                case"-":
                    self.tkdisplaystr.set("Subtractions")
                case"*":
                    self.tkdisplaystr.set("Multiplications")
                case"/":
                    self.tkdisplaystr.set("Divisions")
            self.problemnumber = 0
            self.correctanswers = 0
            self.after(800,self.nextprobleminseries)
            
            
    # keep track of number of problems
    # is series is complete give feedback about number of correct answers
    # and start new series        
    def nextprobleminseries(self):
        if self.problemnumber < self.numberofproblemsinseries:
            self.generateproblem()
            self.problemnumber += 1
        else:
            self.problemnumber = 0
            self.tkdisplaystr.set(f"{self.correctanswers} OUT OF {self.numberofproblemsinseries} CORRECT")            
            self.correctanswers = 0
            self.after(3000,self.nextprobleminseries)
     
        
    # a button was pressed on the window
    def key(self, keytxt):
        txt = self.tkdisplaystr.get()
        if keytxt in "0123456789":
            if self.level == 0: # user is in the process of selecting new level
                self.setlevel(keytxt)
            else:
                txt += keytxt # user is typing his answer
                self.tkdisplaystr.set(txt)
                self.evaluateanswer(keytxt)
        elif keytxt in self.operators: # user is changing the operator
            self.setoperator(keytxt)   
        elif keytxt=="go": # go to next problem right now
            if self.level == 0: # if level was supposed to be selected, just use 1
                self.level = 1
            self.nextprobleminseries()
        elif keytxt=="set": # start selecting new level
            self.setlevel(keytxt)        

# create an instance of Wizard and start it
toepassing=Wizard()
toepassing.mainloop()
