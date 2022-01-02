import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess



root = tk.Tk()
def main():

    app = ToBinary(root)
    root.mainloop()


class ToBinary:

    def __init__(self,window):
        self.window = window
        self.window.title("Binary Converter")
        self.window.resizable(False,False)
        self.window.state("zoomed")
        self.window.bind("<Escape>",self.cls)
        self.window.bind("<Control-r>",self.rst)

        self.TitleBg = "#00274f"
        self.MainBg = "#000022"
        self.BottomBg = "#000022"
        self.BtnColor = "#002b55"
        self.BtnFg = "#ffffff"
        self.ABtnColor = "#5151ff"

        self.ascii = StringVar()   #This will be the title for the textarea , it will be the title for the input or output textarea based on the user input text
        self.bin = StringVar()      #This will be the title for the textarea, it will be the title for the input or output textarea based on the user input text
        self.MainTitle = StringVar()    #It is the main title

        self.TitleFrame = Frame(self.window,bg = self.TitleBg)
        self.TitleFrame.place(relwidth = 1,relheight=0.13)

        self.MainFrame = tk.Frame(self.window,bg = self.MainBg)
        self.MainFrame.place(rely = 0.13,relheight = 0.75,relwidth=1)

        self.BottomFrame = tk.Frame(self.window,bg = self.BottomBg)
        self.BottomFrame.place(rely = 0.88,relheight = 0.22,relwidth=1)

        self.MainTitle.set("Binary Converter") #Default main title
        self.title = tk.Label(self.TitleFrame,textvariable = self.MainTitle,font=("Courier",72,"bold"),fg = "#00FF00",bg = self.TitleBg)
        self.title.place(relx=0.23)

        self.ascii.set("Input") #Default input textarea title
        self.text = tk.Label(self.MainFrame,textvariable = self.ascii,font=("",25,"bold"),fg = "#00FF00",bg = self.MainBg)
        self.text.place(relx=0.06,rely = 0.03)

        self.bin.set("Output")#default output textarea title
        self.binary = tk.Label(self.MainFrame,textvariable = self.bin,font=("",25,"bold"),fg = "#00FF00",bg = self.MainBg)
        self.binary.place(relx=0.06,rely = 0.47)

        self.inputEntry = tk.Text(self.MainFrame,font = ("", 15), bg = "#00162d", fg = "#00FF00", insertbackground= "white")
        self.inputEntry.place(relx = 0.05,rely = 0.05 + 0.05,relwidth = 0.9, relheight = 0.25)

        self.resetBtn = tk.Button(self.MainFrame,text="Reset",command=self.reset,font=("",20,"bold"),cursor="hand2",underline=0,bg=self.BtnColor, fg = self.BtnFg, activebackground=self.ABtnColor)
        self.resetBtn.place(rely=0.35 + 0.05,relx=0.327 + 0.12,relwidth=0.15)

        self.resultEntry = tk.Text(self.MainFrame,font = ("Courier", 15),state=DISABLED,bg = "#00162d",fg = "#00FF00",cursor="arrow")
        self.resultEntry.place(relx = 0.06 - 0.01,rely = 0.55,relwidth = 0.9, relheight = 0.4)

        self.copy_result = tk.Button(self.MainFrame,text="Copy to Clipboard",command=self.copy_link,font=("",15,"bold"),cursor="arrow",bg=self.BtnColor, fg = self.BtnFg, activebackground=self.ABtnColor, state=DISABLED)
        self.copy_result.place(relx= (0.05+0.9) - 0.15, rely = 0.47,relwidth=0.15)

        self.saveBtn = tk.Button(self.BottomFrame,text="Save",command=self.save,font=("",20,"bold"),cursor="arrow",bg=self.BtnColor, fg = self.BtnFg, activebackground=self.ABtnColor, state=DISABLED)
        self.saveBtn.place(relx = 0.327 + 0.12,rely=0.12,relwidth=0.15)

        self.close = tk.Button(self.BottomFrame,text="Close",command=self.close,font=("",20,"bold"),cursor="hand2",bg=self.BtnColor, fg = self.BtnFg, activebackground=self.ABtnColor)
        self.close.place(rely=0.12,relx=0.427 + 0.225,relwidth=0.15)

        self.transFileBtn = tk.Button(self.BottomFrame,text="Open File",command= self.translate_the_text_in_file,font=("",20,"bold"),cursor="hand2",bg=self.BtnColor, fg = self.BtnFg, activebackground=self.ABtnColor)
        self.transFileBtn.place(relx = 0.327 + 0.12 -0.2,rely=0.12,relwidth=0.15)


        self.inputEntry.bind_all('<Key>',self.translate_event)     #This will help to track the user input everytime the user type on the keyboard, it will help to set all the title including main title, and convert the input text
        self.inputEntry.bind('<BackSpace>', self.backspace_event)  #This will help to update the output 



    def backspace_event(self,event):
        self.resultEntry.config(state=NORMAL)           #enable the output textarea to make a changes
        self.resultEntry.delete(1.0,END)                #this will help to completely delete all character in input textbox and update new output
        self.resultEntry.config(state=DISABLED)         #disable the textarea to avoid changes

        self.change_title_text(default=True)            #This set all the title to default if the input textarea is empty

    def copy_link(self):                #this function is for copying the output text
        self.string_output = self.resultEntry.get(1.0, END)
        subprocess.run("clip", universal_newlines=True, input=self.string_output)
        
        self.copy_label = tk.Label(text="Copied Text", font=("Times New Roman", 15), bg = "#111111", fg="yellow") #After the copying of text, there will be a pop up label
        self.copy_label.place(relx= ((0.05+0.9) - 0.15  + 0.043), rely = 0.43)
        self.window.after(500, self.copied_label_forget)    #after 0.5s the label will be dissappear

    def copied_label_forget(self):
        self.copy_label.place_forget()


    def change_title_text(self, default = False, translate=False):
        if default:     #if the default parameter is set to true, then all title will be set to default
            self.MainTitle.set("Binary Converter")
            self.ascii.set("Input")
            self.bin.set("Output")

        if self.inputEntry.get(1.0, END)[0] in ["0","1"]:       #if the input textarea is containing only 1 and 0s then:
            self.MainTitle.set("Binary --> Text")
            self.ascii.set("Binary")                            #the input textarea title is set to binary
            self.bin.set("Text")                               #the input textarea title is set to text

            if translate:                                       #if the translate parameter is true then it will convert the input to text
                self.translate_to_text()
            
        if self.inputEntry.get(1.0, END)[0] in [chr(i) for i in range(32,123) if i != 48 and i != 49]:    #if the input textarea containes a letter and number excluding 0(48) and 1(49) then:
            self.MainTitle.set("Text --> Binary")                   
            self.ascii.set("Text")                              #the input textarea title is set to text
            self.bin.set("Binary")                          #the out textarea title is set to binary

            if translate:                        #if the translate parameter is true then it will convert the input to binary
                self.translate_to_binary()


    def binary_text(self, s = " "):                     #This is the main function where the text converted in binary that inside the list and every element is 8 bits.
    	return [bin(ord(x)) [2:].zfill(8) for x in s]



    def translate_event(self,event):            #This will be trigger every key press of the user
        self.resultEntry.config(state=NORMAL)
        self.resultEntry.delete(1.0,END)
        self.resultEntry.config(state=DISABLED)

        self.saveBtn.config(state=DISABLED, cursor="arrow")         
        self.copy_result.config(state=DISABLED, cursor="arrow")

        self.change_title_text(default=True,translate=True) #it will translate the input every key press and it will set the title to default  if the input textarea is empty


    def translate_to_binary(self):
    	self.resultEntry.config(state=NORMAL)
    	self.resultEntry.delete(1.0,END)

    	for i in range(len(self.binary_text(self.inputEntry.get(1.0,END))) - 1):                #There is minus 1 to not include the white spaces or its corresponding binary in result entry
    		self.resultEntry.insert(tk.END,self.binary_text(self.inputEntry.get(1.0,END))[i]+" ")       #This will display the binary in result entry with spacing in each element of the list. 

    	self.resultEntry.config(state=DISABLED)         #after displaying the output in the result entry, the result entry will be disable to avoid making changes.
    	self.saveBtn.config(state=NORMAL, cursor="hand2")       #These two button will be enable when there is an output, otherwise not.
    	self.copy_result.config(state=NORMAL, cursor="hand2")


    def reset(self):
        self.resultEntry.config(state=NORMAL)               # the result entry will be enable to delete or reset the text in the result entry
        self.resultEntry.delete(1.0,END)
        self.inputEntry.delete(1.0,END)
        self.resultEntry.config(state=DISABLED)
        self.saveBtn.config(state=DISABLED, cursor="arrow")         #the save and copy button will be disable because there is no output after resetting.
        self.copy_result.config(state=DISABLED, cursor="arrow")

        self.change_title_text(default=True)        #all the title will  be default because there is no input or output.


    def save(self):
        choice = messagebox.askyesno("Save", "Save only output?")
        file_path = filedialog.asksaveasfilename(title = " Save As", filetypes=[("Text",".txt"),("All Files",".*")],defaultextension='.txt',confirmoverwrite=True)
        
        if file_path is None:
            return
        
        if choice:              #if the user done choosing location, naming a file and the user pick the save output only then:
            with open(file_path, "w") as f:         #it will open a  file and
                for i in range(len(self.resultEntry.get(1.0,END))):         #get all the text in result entry and write on the file
                    f.write(self.resultEntry.get(1.0,END)[i])

        else:                   #if the user want to save all including the text in input entry then:
            file = open(file_path,"w")
            file.write(self.MainTitle.get().split(" -")[0])         #This will  be the title for the input 
            file.write("\r\n{}".format(self.inputEntry.get(1.0,END)))       #This is the input
            file.write("\r\n%s\r\n" % (self.MainTitle.get().split("> ")[1]))    #This is the title for the output
            
            for i in range(len(self.resultEntry.get(1.0,END))):         #this will be the output
                file.write(self.resultEntry.get(1.0,END)[i])
                
            file.close()
            
        messagebox.showinfo("Done","File Saved")
        self.save = True

    
    def rst(self,event):        #This will be triggered if the user press the ctrl+r
        self.reset()


    def cls(self,event):        #This will be triggered if the user press the escape key
        self.close()

    
    def translate_to_text(self):        #Translating the binary to text
    
        self.resultEntry.config(state=NORMAL)
        self.resultEntry.delete(1.0,END)
        self.resultEntry.config(state=DISABLED)
        
        self.input = self.inputEntry.get(1.0,END).strip()      #This will be remove the whtiespaces in the start and end of the input
        self.input2 = self.input.split(" ")        #The input which is binary will be converted to list and every element contains of 8bits
        self.ascii_sentence = ""
        
        try:                    #there is an  try and except block because the only valid element is length of 8 and there is a possibility that the element contains less than or greater than 8
            for bins in self.input2:            #this will loop over the binary list
                _chr = int(bins,2)              #each element will be converted into numbers. for example: 01000001 --> 65
                ascii_chr = chr(_chr)           #the numbers will be converted into letters or characters. for example: chr(65) --> A
                self.ascii_sentence += ascii_chr    #this will add all the character to forom a sentence or word.
                
        except ValueError:
            pass
        
        self.resultEntry.config(state=NORMAL)           #the result entry will be enable in order to put an output
        self.resultEntry.insert(tk.END,self.ascii_sentence)     #this will write the output in result entry.
        self.resultEntry.config(state=DISABLED)         #the result entry will be disable again to avoid making changes
        
        if len(self.resultEntry.get(1.0,END)) != 0:     #these two button will be enable when there is an output, otherwise this will be disable
            self.saveBtn.config(state=NORMAL, cursor="hand2")
            self.copy_result.config(state=NORMAL, cursor="hand2")



    def translate_the_text_in_file(self):               #translating the text inside the text file
        chosen_filename = filedialog.askopenfilename(filetypes=[("Text",".txt"),("All Files",".*")])        #the user will pick the text while that the user wants to be translated
        is_text = False

        if chosen_filename is None:
            return

        with open(chosen_filename, 'r') as f:       #this will open the file
            self.resultEntry.delete(1.0,END)        
            self.inputEntry.delete(1.0,END)

            for line in f:                          #it will read every line in a file
                self.inputEntry.insert(tk.END, line)        #it will write all the text in a file in a input entry

                for i in range(len(line)):          #this loop is for reading every character in every line
                    if line[i] in [chr(j) for j in range(32,123) if j != 48 and j != 49]:       #if the computer finds that there are letter in a line the in will be consider as the text
                       is_text = True 

                    else:                                       #otherwise it's binary
                        is_text = False


            if is_text:     #if it is a text then it will change the title to "Text --> Binary" and the translate parameter is true which means that after chaging the title the text will be converted to binary
                self.change_title_text(translate=True)

                
            if not is_text:             #if it's binary then:
               self.inputEntry.delete(1.0,END)      #the input entry will be none because the chosen file by the user will be read again in 'translate_the_binary_in_file' function
               self.translate_the_binary_in_file(chosen_filename)   
            
                
    def translate_the_binary_in_file(self, file):       #this function will translate the binary in a file to text
        text = ""
        start_pos = 0
        trim_text = ""

        with open(file, 'r') as f:      
            for line in f:          #all line in a text file will be converted into 1 single string
                text += line

        text_with_no_white_spaces = "".join(text.split())        #this will be remove all the white spaces in a string

        for i in range(len(text_with_no_white_spaces)):     #this will read every bit on the string
            if i % 8 == 0 and i != 0:           #it means that the i is divisible by 8 then it will add spaces after it because every letter or number is 8 bits in binary. There is i != 0 because 0 % 8 == 0
                trim_text += text_with_no_white_spaces[start_pos:i] + " "       #For example: [0:8],[8:16], [16:24],
                start_pos += 8                  #the start pos will be increment by 8 because in the above comment

        self.inputEntry.insert(tk.END, trim_text) # it will display the valid format of binary in input entry
        self.change_title_text(translate=True)  #and the title will be change and it will convert the input to text

    
    def close(self):
        if(self.save == True):
            a = messagebox.askquestion("Close","Do you really want to close")       #if the user save his work and planning to close this app then only this messagebox will be show
            if a == "yes":      #if the user say yes then the app will be close
                self.window.destroy()
                
        else:   #if the user does not save his work and planning to close the app then:
            if len(self.resultEntry.get(1.0, END)) > 1:             #if there are output and input then:
                b = messagebox.askquestion("Close","Do you want to save it?")       #this messagebox will be show
                if b == "yes":      
                    self.save()
                    
                self.window.destroy()       #after saving the file or not, it will close the window
                
            else:   #if there is no output then:
                a = messagebox.askquestion("Close","Do you really want to close?")      #this messagebox will be only show
                if a == "yes":
                    self.window.destroy()


if __name__ == '__main__':
    main()


