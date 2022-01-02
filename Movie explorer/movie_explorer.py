from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import glob
import os
import random
import math
import threading
import pyautogui as pg
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

root = tk.Tk()

leftFrame_bg = "#4B6F97"
mainFrame_bg = "#2C466A"
movie_container_border_color = "#000"
movie_container_bg = "#294161"
button_bg = "#000000"

movie_container_fg = "#76ABDC"
title_and_button_fg = "#76ABDC"
left_frame_fg = "#2B4057"


def main():
     app = Main(root)
     root.mainloop()


class Main:
     def __init__(self, window):
          self.window = window
          self.window.title("Watch")
          self.window.config(bg="black")
          self.window.attributes("-fullscreen", True)
          #self.window.iconphoto(True, tk.PhotoImage(file = "icon.png"))
          self.path = ""

          self.titleFrame = tk.Frame(root, height=150, width=10000)
          self.leftFrame = tk.Frame(root, bg = leftFrame_bg, height=150, width=400)
          self.mainFrame = tk.Frame(root, bg= mainFrame_bg)
          self.textFrame = tk.Frame(self.mainFrame,width=1500, height=1, bg= movie_container_border_color)
          self.movie_container  = tk.Listbox(self.textFrame, bg = movie_container_bg, fg = movie_container_fg, font = ("Verdana", 14),width=120, height=23, activestyle='none', cursor = "hand2", bd=5)

          self.title = tk.Label(self.titleFrame, bg= movie_container_border_color, text="Watch Movies", font=("AR DESTINE",56), fg=title_and_button_fg)
          
          self.title.pack(fill=BOTH)
          self.titleFrame.pack( padx = 20, pady = (10,0))
          self.leftFrame.pack(fill="both", padx = (20,0), pady=(0,30), side="left")
          self.mainFrame.pack(fill="both", expand="yes" , padx=(10,20), pady=(0,30), side="right")  
          self.textFrame.pack(padx=30, pady=20)
          self.movie_container.pack(padx= 15, pady=15, side="left")

          self.indexxx = 0 
          self.delete_count = 1
          self.titleList = []
          self.appending_movie = []
          self.back_button_exist = False
          self.back_click = False
          self.btn_changePath_exist = False

          self.check_if_path_exist()


     def set_volume(self,level):
          devices = AudioUtilities.GetSpeakers()
          interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
          volume = cast(interface, POINTER(IAudioEndpointVolume))
          volume.SetMasterVolumeLevel(level, None)


     def check_if_path_exist(self, change_path=False):
          self.change_path = change_path
          self.line = ""

          if "path.txt" not in os.listdir(".\\"):
               with open("path.txt", "w"):
                                pass
     
          with open(".\\path.txt", "r") as f:
               for self.path in f:
                    self.line += self.path

          if len(self.line) != 0 and self.change_path == False:
               self.read_path_file()

          if len(self.line) == 0 or self.change_path == True:
               if self.change_path == True:
                    self.movie_container.delete(0, 'end')
                    self.random_play.pack_forget()
                    self.main_folder_title.pack_forget()
                    self.Btnexit.pack_forget()
                    self.Bchange_path.pack_forget()

               self.input_text = tk.Label(self.mainFrame, text= "Enter Path:", font = ("Verdan", 17), bg="#2C466A", fg = title_and_button_fg )
               self.ask_field = tk.Entry(self.mainFrame, width= 20 , font=("Times New Roman", 17))
               self.submit = tk.Button(self.mainFrame, command=self.get_path, text="Submit",bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 15), cursor="hand2",borderwidth=5,activebackground="#76ABDC")
               
               self.input_text.pack(padx=(420,10), side=LEFT)
               self.ask_field.pack(side=LEFT)
               self.submit.pack(padx= 28, side=LEFT)
               self.ask_field.bind("<Return>", func= lambda e:self.get_path())

          
     def display_button_text(self, path, main_title_exist = False):
          self.path = path
          self.main_title_exist = main_title_exist

          self.watch = Watchs(self.path)
          self.display_text(self.watch.list_movie)
          self.listbox_item = [item[item.index('> ') + 2:] for item in self.movie_container.get(0, self.movie_container.size() - 1)]

          self.random_play = tk.Button(self.mainFrame, command=lambda:self.random_movie(self.listbox_item), text="Random Play", bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 25), cursor="hand2",borderwidth=5,activebackground=title_and_button_fg)
          self.random_play.pack(padx=(470,15), side="left")

          if self.main_title_exist:
               return

          self.main_folder_title = tk.Label(self.leftFrame, text=self.line.split("\\")[-1].capitalize() , fg = "#2B4057", bg = "#4B6F97", font=("Verdana", 23) )
          self.main_folder_title.pack(pady= (15,0), side="top")

          if not self.btn_changePath_exist:
               self.Bchange_path = tk.Button(self.leftFrame, command=lambda:self.check_if_path_exist(change_path = True), text="Change Path", bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 20), cursor="hand2",borderwidth=5,activebackground=title_and_button_fg)
               self.Bchange_path.pack(padx = 100, pady = 20,side="bottom")

          self.btn_changePath_exist = True

          
     def read_path_file(self, change_path = False):
          self.line = ""
          with open(".\\path.txt", "r") as f:
               for path in f:
                    self.line += path

          if change_path:
               return self.line

          else:
               self.display_button_text(self.line)

     def get_path(self):
          self.path = self.ask_field.get()
          self.btn_changePath_exist = False

          if os.path.exists(self.path):
               with open(".\\path.txt", "w") as f:
                    f.write(self.ask_field.get())

               self.ask_field.pack_forget()
               self.submit.pack_forget()
               self.input_text.pack_forget()

               self.main_folder_title = tk.Label(self.leftFrame, text=self.path.split("\\")[-1].capitalize() , fg = left_frame_fg, bg = leftFrame_bg, font=("Verdana", 23) )
               self.main_folder_title.pack(pady= (15,0), side="top")

               try:
                    self.Bchange_path.pack_forget()
               except:
                    pass

               self.Bchange_path = tk.Button(self.leftFrame, command=lambda:self.check_if_path_exist(change_path = True), text="Change Path", bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 20), cursor="hand2",borderwidth=5,activebackground="#76ABDC")
               self.Bchange_path.pack(padx = 100, pady = 20,side="bottom")
               self.btn_changePath_exist = True

               self.display_button_text(self.ask_field.get(), main_title_exist = True)
               
          else:
               self.ask_field.delete(0, 'end')
               messagebox.showerror("Invalid", "Path doesn't exist")
               

     def exit(self):
          root.destroy()


     def display_folder_title(self, title_name = "", play_with_random=False):
          self.title_name = title_name
          self.label1 = ""
          self.label2 = ""
          self.label3 = ""
          self.label4 = ""
          self.label5 = ""
          self.label6 = ""
          self.temp_titleList = [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6]

          title_len = len(self.title_name)

          self.font_size = 20
          
          if title_len > 24:
               self.font_size = 20 - int((title_len- 20)/2)
               
          
          if not play_with_random:
               self.label = tk.Label(self.leftFrame, text= "|\n" + self.title_name , fg = left_frame_fg, bg = leftFrame_bg, font=("Verdana", self.font_size) )
               self.label.pack(side="top")

               self.emptyLabel = tk.Label(self.leftFrame, text=" " * 50, bg = leftFrame_bg, fg = left_frame_fg, font=("", self.font_size) )
               self.emptyLabel.pack(side="bottom")

               self.temp_titleList[self.indexxx] = self.label
               self.titleList.append(self.temp_titleList[self.indexxx])
                         
               self.indexxx += 1
                    

     def setVariableToDefault_in_backEvent(self):
          self.delete_count = 1
          self.appending_movie = []
          self.titleList = []
          self.back_click = False
          self.delete_label_in_left_frame()
     

     def back_event(self):
          self.indexxx = 0
          self.back_click = True
          self.btn_changePath_exist = False
          self.delete_label_in_left_frame()
          self.emptyLabel.destroy()

          for file in self.appending_movie[:-1 * self.delete_count]:
               self.display_folder_title(title_name=file)

          self.update_path = "\\".join(self.line.split("\\") + self.appending_movie[:-1 * self.delete_count])
          self.updated_movie_list = [movie for movie in os.listdir(self.update_path) if os.path.isdir(self.update_path + "\\" +movie) or ".mp4" in movie or ".MP4" in movie]

          if self.update_path == self.line:
               self.listbox_update(self.watch.display(self.watch.list_movie))
               self.display_text(self.watch.list_movie)
               self.back.pack_forget()
               self.setVariableToDefault_in_backEvent()     
               return

          self.listbox_update(self.watch.display(self.updated_movie_list))
          self.display_text(self.updated_movie_list)

          self.delete_count += 1
          

     def delete_label_in_left_frame(self):
          for label in self.titleList:
               label.pack_forget()

     def play_movie(self,movie):
          try:
               os.system("TASKKILL /F /IM vlc.exe")
          except:
               pass


          os.system(f"\"{movie}\"")


     def check_movie(self, evt, movie_in_folder):
          try:
               self.w = evt.widget
               self.index = int(self.w.curselection()[0])
               self.movie = self.w.get(self.index)
               self.movie2 = (self.movie[self.movie.index('>') + 2:])
          except :
               return

          if ".mp4" in self.movie:
               t1 = threading.Thread(target=self.play_movie,args=(self.watch.source[self.movie2],))
               t1.start()
               time.sleep(6)
               pg.moveTo(500,500)
               pg.doubleClick()
               self.set_volume(-10)
               
               
                              
          else:
               self.back_click= False
               self.movie_from_list = []

               try:
                    self.emptyLabel.destroy()
               except:
                    pass

               if self.back_click:
                    self.delete_count -= 1

               if self.movie2 not in self.appending_movie:
                    self.appending_movie.append(self.movie2)

               self.read_path_file(change_path=True)
               self.full_path_of_certain_dir_or_movie = "\\".join(self.line.split("\\") + (self.appending_movie))
               
               for movie in os.listdir(self.full_path_of_certain_dir_or_movie):
                    if os.path.isfile(self.full_path_of_certain_dir_or_movie + "\\" + movie):
                         if ".mp4" in movie:
                              self.movie_from_list.append(movie)
                              continue
                         continue
     
                    self.movie_from_list.append(movie)

               self.display_folder_title(title_name=self.appending_movie[-1])
               self.listbox_update(self.watch.display(self.movie_from_list))
               self.display_text(self.movie_from_list)

               if self.back_button_exist:
                    return

               self.Btnexit.pack_forget()
               self.Bchange_path.pack_forget()

               self.back = tk.Button(self.mainFrame, command=self.back_event, text="Back" ,bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 25), cursor="hand2",borderwidth=5,activebackground="#76ABDC")
               self.back.pack(padx=(0,50) , side="left")
               self.back_button_exist = True

          
     def listbox_update(self,data):
          self.movie_container.delete(0,'end')
          for item in data:
               self.movie_container.insert(END, item)

          self.listbox_item = [item[item.index('> ') + 2:] for item in self.movie_container.get(0, self.movie_container.size() - 1)]

     def random_movie(self, movie_list):
          self.movie_list = movie_list

          r = random.randrange(0, len(movie_list) - 1)
          self.movie = self.movie_list[r]

          if ".mp4" in self.movie:
               os.system((f"\"{self.watch.source[self.movie]}\""))
               [label.pack_forget() for label in self.display_folder_title(play_with_random=True)]

          else:
               self.random_movie(self.movie) 


     def display_text(self, movie_in_folder):
          def temp_check(event, self=self, movie_in_folder = movie_in_folder):
               return self.check_movie(event, movie_in_folder)

          self.movie_container.delete(0,'end')

          for i in range(len(self.watch.display(movie_in_folder))):
               self.movie_container.insert(END, self.watch.display(movie_in_folder)[i])

          if movie_in_folder == self.watch.list_movie:
               self.back_button_exist = False
               self.Btnexit = tk.Button(self.mainFrame, command=self.exit, text="Exit" ,bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 25), cursor="hand2",borderwidth=5,activebackground="#76ABDC")
               self.Btnexit.pack(padx=(0,50) , side="right")

               
               if not self.btn_changePath_exist:
                    self.Bchange_path = tk.Button(self.leftFrame, command=lambda:self.check_if_path_exist(change_path = True), text="Change Path", bg = button_bg, fg=title_and_button_fg, font = ("Verdana", 20), cursor="hand2",borderwidth=5,activebackground="#76ABDC")
                    self.Bchange_path.pack(padx = 100, pady = 20,side="bottom")

                    self.btn_changePath_exist = True

          self.scrollbar = Scrollbar(self.textFrame)
          self.scrollbar.config(command=self.movie_container.yview)
          
          self.movie_container.bind('<Double-Button>', temp_check)
          self.movie_container.bind('<Return>', temp_check)


class Watchs:
     def __init__(self, path):
          self.path = path
          self.all_movie = glob.glob(f"{path}\\**\\*.mp4", recursive = True) 

          self.movie_location = [self.movie.split("\\") for self.movie in self.all_movie]
          self.full_location = [self.movie for self.movie in self.all_movie]
          self.name_movie = [self.movie.split("\\")[-1] for self.movie in self.all_movie]

          self.scan()
          self.list_movie = self.getAllMovie()
          self.list_movie.sort()

          self.source = self.source()


     def speech(self, msg):
          pass


     def getMainFolder(self):
          return self.path.split("\\")[-1]

     
     def source(self):
          self.movie_dict = {}
          for i in range (len(self.all_movie)):
               self.movie_dict[self.name_movie[i]] = f"{self.full_location[i]}"

          return self.movie_dict


     def getMovie_in_SubFolder(self, num):
          self.subFolder = self.movie_location[num][self.movie_location[num].index(self.getMainFolder()) + 1]
          return self.subFolder


     def scan(self):
          self.already_print = []
          self.sub_movie2 = []
          self.movie_folder = []
          self.displayAll = [] 
          self.count = 0

          for i in range(len(self.movie_location)-1):
               if i > 0:
                    if(os.path.isdir(self.path + "\\" + self.getMovie_in_SubFolder(i+1))):
                         if (self.getMovie_in_SubFolder(i) == self.getMovie_in_SubFolder(i + 1) or self.getMovie_in_SubFolder(i) == self.getMovie_in_SubFolder(i - 1)):
                              if self.getMovie_in_SubFolder(i) not in self.already_print:
                                        self.already_print.append(self.getMovie_in_SubFolder(i))
                                        self.movie_folder.append(self.getMovie_in_SubFolder(i))

                              if (self.getMovie_in_SubFolder(i) == self.getMovie_in_SubFolder(i + 1) or self.getMovie_in_SubFolder(i) == self.getMovie_in_SubFolder(i - 1)):
                                   if self.count == 0:
                                        self.sub_movie2.append(self.name_movie[i])
                                        self.count += 1
                                        continue
                                   
                                   self.sub_movie2.append(self.name_movie[i])

                              else:
                                   self.sub_movie2.append(self.name_movie[i])
                                   self.count = 0                                                      
    

          for self.movie in self.name_movie:
               self.fullPath = "{}\\{}".format(self.path, self.movie)

               if os.path.isdir(self.fullPath):
                    if len(os.listdir(self.fullPath)) == 0:
                         continue

               if self.movie not in self.sub_movie2:
                    self.displayAll.append(self.movie)

          for movie in self.movie_folder:
               self.displayAll.append(movie)
          
          self.displayAll.sort()


     def display(self,movie_in_folder):
          self.movie_in_folder = movie_in_folder
          self.my_list = []
          self.all_text = ""

          for i in range(len(self.movie_in_folder)):
               if self.movie_in_folder == self.list_movie:
                    self.my_list.append(f'[{str(i)}]  ---> ' + str(self.movie_in_folder[i]))
               
               else:
                    self.my_list.append(f'[{str(i)}]  ---> ' + str(self.movie_in_folder[i]))

          return self.my_list

     def getAllMovie(self):
          return self.displayAll



if '__main__' == __name__:
     main()

