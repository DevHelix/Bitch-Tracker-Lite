# gui -> create new box (hoes) -> type, hair color, rating -> adds it to data table  -> save it to a text file

# COMPLETED: 8/18/2022

# intended to keep track of all of your hoes
from asyncio import gather
from multiprocessing.util import info
import tkinter as tk
from tkinter import* # imports EVERYTHING from tkinter
from tkinter import ttk
from turtle import width
from PIL import ImageTk, Image
import time


class Ho: # NOTE: ADDING SELF. TO EVERY VARIABLE PREVENTS IT FROM BEING GARBAGE COLLECTED, OTHERWISE THE VARIABLE WOULDN'T WORK
    def __init__(self, root, **kwargs): # NOTE: you can change the x,y of an object by using the place method
        self.root = root
        blank_space = " "
        self.root.title(160 * blank_space + "Bitch-Tracker Lite")
        self.root.geometry("1170x580+0+0")
        self.root.resizable(0,0)
        self.old_value = ''

        style= ttk.Style()
        style.configure('style.TEntry', 

            fieldbackground="azure3", 

            foreground="azure2"           

           )

        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground= "azure3", background= "azure2")

        # okay the module is old asf so everything will look like ass, but here's the rundown when making a new frame
        # first you call the frame function defining that it is a gui frame
        # then the arguments in frame are (what the frame will be parented to, the width of the border, width and height of the frame
        # then relief which is best defined here https://www.tutorialspoint.com/python/tk_relief.htm,
        # and finally the color of the frame, got all that? then you do [frameName].grid() so it shows up on the screen)

        self.mainFrame = Frame(self.root, bd=10, width=1350, height=800, relief=RIDGE, bg="azure4")
        self.mainFrame.grid()

        topFrame1 = Frame(self.mainFrame, bd=0,width=1350,height=70)  
        topFrame1.grid(row=1,column=0) 

        titleFrame = Frame(self.mainFrame, bd=0,width=1350,height=70)
        titleFrame.grid(row=0,column=0)

        self.centerFrame = Frame(topFrame1, bd=2, width=1350, height=400, relief=RIDGE,bg="azure3")
        self.centerFrame.grid(row=2,column=0)

        self.inputsFrame = tk.Frame(self.centerFrame, bd=1,width=700,height=10,relief=RIDGE, bg="azure3")
        self.inputsFrame.grid(row=0,column=0)

        self.dataFrame = Frame(self.centerFrame, bd=1,width=800,height=500,relief=RIDGE, bg="azure3")
        self.dataFrame.grid(row=0,column=1)
        self.dataFrame.grid_propagate(False) # prevents frame from shrinking (it shrinks relative to the widgets inside it)

        self.labelTitle = Label(titleFrame,font = ('Bahnschrift Light', 30), text='Bitch-Tracker Lite',bd=5,bg='azure2',padx=132)
        self.labelTitle.grid(row=0,column=0)

        self.NameLabel = Label(self.inputsFrame,font = ('Bahnschrift Light', 17), text='Name: ', bd=5, anchor=W, bg="azure3")
        self.NameLabel.grid(row=0,column=0,padx=20)

        self.NameStringVar = tk.StringVar()
        self.NameInput = Entry(self.inputsFrame,textvariable=self.NameStringVar,font = ('Bahnschrift Light', 17), bg="white", width=16, justify='left')
        self.NameInput.grid(row=0,column=1)

        self.NameStringVar.trace('w',self.max)
        self.NameGet, self.NameSet = self.NameStringVar.get, self.NameStringVar.set

        self.string_var = tk.StringVar()
        self.AgeLabel = Label(self.inputsFrame,font = ('Bahnschrift Light', 17), text='Age: ', anchor=W, bg="azure3")
        self.AgeLabel.grid(row=1,column=0,padx=20)
        
        self.AgeInput = Entry(self.inputsFrame, textvariable=self.string_var, font = ('Bahnschrift Light', 17), width=16, justify='left')
        self.AgeInput.grid(row=1,column=1)
        
        self.string_var.trace('w',self.check)
        self.get, self.set = self.string_var.get, self.string_var.set

        self.ClassLabel = Label(self.inputsFrame,font = ('Bahnschrift Light', 17), text='Class: ', anchor=W, bg="azure3")
        self.ClassLabel.grid(row=2,column=0,padx=20)

        self.ClassComboBox = ttk.Combobox(self.inputsFrame,font = ('Bahnschrift Light', 17),state='readonly',width=15)
        self.ClassComboBox['values'] = ('','Freshman','Sophomore','Junior','Senior','Under-Freshman','Over-Senior')
        self.ClassComboBox.current(0)
        self.ClassComboBox.grid(row=2,column=1)
        

        self.GenderLabel = Label(self.inputsFrame,font = ('Bahnschrift Light', 17), text='Gender: ', anchor=W, bg="azure3")
        self.GenderLabel.grid(row=3,column=0,padx=20)

        self.GenderComboBox = ttk.Combobox(self.inputsFrame,font = ('Bahnschrift Light', 17),state='readonly',width=15)
        self.GenderComboBox['values'] = ('','Male','Female','Other')
        self.GenderComboBox.current(0)
        self.GenderComboBox.grid(row=3,column=1)
        

        self.RatingLabel = Label(self.inputsFrame,font = ('Bahnschrift Light', 17), text='Rating: ', anchor=W, bg="azure3")
        self.RatingLabel.grid(row=4,column=0,padx=20)

        self.RatingComboBox = ttk.Combobox(self.inputsFrame,font = ('Bahnschrift Light', 17),state='readonly',width=15)
        self.RatingComboBox['values'] = ('','1','2','3','4','5','6','7','8','9','10')
        self.RatingComboBox.current(0)
        self.RatingComboBox.grid(row=4,column=1)
        
        self.enterButton = ttk.Button(self.inputsFrame,text="Submit",width=7, command= self.Gather_Data)
        self.enterButton.grid(row=6,column=1)
        
        #self.warnlabel = tk.Label(self.inputsFrame,font = ('Bahnschrift Light', 13), text='ERROR: Empty Entry', anchor=N, bg="red",width=20)
        #self.warnlabel.grid(row=6,column=0,in_=self.inputsFrame)
        #self.warnlabel.grid_remove()
        
        all_Data = []

        with open('data.txt','r') as file:
            f = file.readlines()
            for line in f:
                alteredLine = line.replace(',',' ')
                finalData = alteredLine.split()
                all_Data.append(finalData)
                Name_Data = finalData[0]
                Age_Data = finalData[1]
                Class_Data = finalData[2]
                Gender_Data = finalData[3]
                Rating_Data = finalData[4]

        if len(all_Data) > 0:
            for i,dataLine in enumerate(all_Data):

                self.infoFrame = Frame(self.dataFrame, bd=1,width=785,height=30)
                self.infoFrame.grid(row=i,column=0,pady=4,padx=10)
                self.infoFrame.grid_propagate(False)

                if dataLine[1].isdigit(): # in case there are any spaces in the name
                    
                    nameLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Name: {dataLine[0]}',width=14,anchor=W,justify=LEFT,)
                    nameLabel.grid(row=0,column=0,in_=self.infoFrame)

                    ageLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Age: {dataLine[1]}',width=9,anchor=W)
                    ageLabel.grid(row=0,column=1,padx=20)

                    classLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Class: {dataLine[2]}',width=17,anchor=W, justify=LEFT)
                    classLabel.grid(row=0,column=2,padx=20)

                    genderLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Gender: {dataLine[3]}',width=17,anchor=W)
                    genderLabel.grid(row=0,column=3,padx=20)

                    genderLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Rating: {dataLine[4]}',width=17,anchor=W)
                    genderLabel.grid(row=0,column=4,in_=self.infoFrame)
                else: # incase there are a first and last name
                    
                    nameLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Name: {(dataLine[0]+" "+dataLine[1])}',width=18 ,anchor=W,justify=LEFT)
                    nameLabel.grid(row=0,column=0,in_=self.infoFrame)

                    ageLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Age: {dataLine[2]}',width=8,anchor=W)
                    ageLabel.grid(row=0,column=1,padx=20)

                    classLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Class: {dataLine[3]}',width=17,anchor=W, justify=LEFT)
                    classLabel.grid(row=0,column=2,padx=20)

                    genderLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Gender: {dataLine[4]}',width=17,anchor=W)
                    genderLabel.grid(row=0,column=3,padx=20)

                    genderLabel = Label(self.infoFrame,font = ('Bahnschrift Light', 13), text=f'Rating: {dataLine[5]}',width=17,anchor=W)
                    genderLabel.grid(row=0,column=4)
                

    def Gather_Data(self,a=0, *args):
       
        self.NameResult = self.NameInput.get()
        self.AgeResult = self.AgeInput.get() # age var for string var
        self.ClassResult = self.ClassComboBox['values'][self.ClassComboBox.current()]
        self.GenderResult = self.GenderComboBox['values'][self.GenderComboBox.current()]
        self.RatingResult = self.RatingComboBox['values'][self.RatingComboBox.current()]

        self.results = (self.NameResult,self.AgeResult,self.ClassResult,self.GenderResult,self.RatingResult)

        #print("Name: ",self.NameResult,
        #"\n","Age: ",self.AgeResult,
        #"\n","Class: ",self.ClassResult,
        #"\n","Gender: ",self.GenderResult,
        #"\n","Rating: ",self.RatingResult)

        if int(self.old_value) <= 12 or self.ClassResult == "Under Freshman":
            
            self.caught1 = PhotoImage(file = r"C:\Users\vince\Desktop\Project A - HoTracker\imgs\caught2.png")
        
            CaughtFrame = Canvas(self.dataFrame, height=500,width=500)
            CaughtFrame.grid()

            bg = Label(CaughtFrame, image = self.caught1, height=500,width=500)
            bg.grid()

            self.labelTitle.config(text="YES OFFICER, THIS MAN RIGHT HERE",font=('Bahnschrift Light', 30), bg="red",bd=0)
            self.labelTitle.config(bg = "blue" if a & 1 else "red")
            self.labelTitle.after(400,self.Gather_Data, a ^ 1 )

        self.count = 0 # literally no other way i can think of to check if the boxes aren't empty (that's efficient)

        for x in(self.results):
            if str(x) != '':
                self.count = self.count + 1
       
        if self.count == 5: # confirms that all entries are filled
            print("Success")
            with open('data.txt','a') as f: # appending line
                self.dataString = ''
                for i in(self.results):

                    self.dataString = self.dataString + ',' + str(i)# adds the comma so data can be spliced later
                    
                f.write(self.dataString+"\n")
                print(self.dataString)
            self.mainFrame.destroy() # refreshes and updates the ui to add data to the dataframe
            self.__init__(root)


        else: # one or more entries are empty
            print("fail")
            #self.warnlabel.grid() # raises the label to reveal it
            #root.after(3000, root.destroy())
            
            
   
    def check(self, *args): # prevents letters in the age entry form
        if self.get().isdigit() and len(self.get()) <= 3: # ensures the input is an integer and limits the char count to 3
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.set(self.old_value)

    def max(self, *args): # for the name entry form
        count = 0
        for i in self.NameGet():
            if i == ' ':
                count += 1

        if len(self.NameGet()) <= 17 and count <= 1: # limits the char count to 17, also limits to the max num of spaces to 1, so as the data doesn't break
            self.old_value = self.NameGet()
        else:
            self.NameSet(self.old_value)


if __name__ == '__main__':
    root = Tk()
    application = Ho(root)
    root.mainloop()
