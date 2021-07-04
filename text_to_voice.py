import re
import tkinter as tk
from tkinter import font as tkfont  
from tkinter import messagebox
import mysql.connector as connector
from PIL import ImageTk, Image
from tkinter import filedialog
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

############################################ Database Connection ############################################
class DBHelper():
    def __init__(self):
        self.con = connector.connect(user = 'root',
                                    host = 'localhost',
                                    password = 'pass12345PASS',
                                    port='3306',
                                    database = 'stt')

    #INSERT DATA
    def insert_user(self, name ,username, email, password):
        try: 
            query = "INSERT INTO users( name, username ,email,password,status) values('{}','{}','{}','{}',{})". format(name, username, email,password,1)
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
            cur.close()
            success = "USER SUCCESSFULLY SAVED"
            return success
            
        except Exception as es:
            error = "This Email is already exist by another User"
            return error
    
    def Fetch_by_email(self, email, password):
        try:
            query = "SELECT * FROM users WHERE email ='{}'". format(email)
            cur = self.con.cursor()
            cur.execute(query)
            c = cur.fetchall()
            if len(c) == 0:
                error = "RECORD NOT FOUND"
                return error
            else:
                if c[0][4]== password:
                    success = "LOGIN SUCCESSFULL"
                    cur.close()
                    return success
                else:
                    error = "Incorrect Password"
                    cur.close()
                    return error
        except Exception as es:
            error = f"ERROR DUE TO: {str(es)}"
            return error
    def Fetch_All(self):
        try:
            query = "SELECT * FROM users"
            cur = self.con.cursor()
            cur.execute(query)
            c = cur.fetchall()
            if len(c) == 0:
                error = "Table is empaty"
                return error
            else:
                return c
        except Exception as a:
            print("\n\tStudent Could not find. THANKS\n\t",a)

############################################ Main Class ############################################
class Mian(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Signup, Login, Dashboard, Profile):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Signup")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

############################################ Signup PAGE ############################################
class Signup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ####################### Create Window #######################
        self.controller .title('Text to speach')
        self.controller.geometry('1000x600')
        self.controller.resizable(0, 0)

        ####################### Create 1st canvas #######################
        self.canvas1 = tk.Canvas(
            self,
            bg="#1b1063",
            width=700,
            height=1000
        )
        self.canvas1.place(x=-20, y=-20)

        ####################### Put image on 1st canvas #######################
        self.tkimage = ImageTk.PhotoImage(Image.open("1.png"))
        self.canvas1.create_image(
            -230,
            0,
            image=self.tkimage,
            anchor=tk.NW
        )
        ####################### Write Welcome text #######################
        self.canvas1.create_text(
            370,
            100,
            text="Speech To Text With AI",
            fill="white",
            font=('Helvetica 15 bold')
        )
        ####################### Create 2nd canvas #######################
        self.canvas2 = tk.Canvas(
            self,
            bg="white",
            width=700,
            height=1000
        )
        self.canvas2.place(x=680, y=-20)
        ####################### Write Sign up text #######################
        self.canvas2.create_text(
            170,
            100,
            text="Sign Up",
            fill="black",
            font=('Helvetica 15 bold')
        )

        ####################### Name and its field #######################
        self.text_canvas1 = self.canvas2.create_text(60, 190, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas1, text="Name", font=(20))
        self.entry1 = tk.Entry(self)
        self.canvas2.create_window(170, 200, window=self.entry1)

        ####################### Username and its field #######################
        self.text_canvas2 = self.canvas2.create_text(30, 220, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas2, text="Username", font=(20))
        self.entry2 = tk.Entry(self)
        self.canvas2.create_window(170, 230, window=self.entry2)

        ####################### Email and its field #######################
        self.text_canvas3 = self.canvas2.create_text(60, 250, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas3, text="Email", font=(20))
        self.entry3 = tk.Entry(self)
        self.canvas2.create_window(170, 260, window=self.entry3)

        ####################### Password and its field #######################
        self.text_canva4 = self.canvas2.create_text(30, 280, anchor="nw")
        self.canvas2.itemconfig(self.text_canva4, text="Password", font=(20))
        self.entry4 = tk.Entry(self, show="*", width=20)
        self.canvas2.create_window(170, 290, window=self.entry4)

        ####################### Sign up Button #######################
        btn1 = tk.Button(
            self,
            text='Signup',
            bg="#99b6ff",
            height=1,
            command = self.insert_userr,
            width=10
        )
        self.canvas2.create_window(170, 350, window=btn1)

        ####################### Drow Line #######################

        self.canvas2.create_line(0, 390, 400, 390)

        ####################### Already have account Login Buuton #######################

        self.login1 = self.canvas2.create_text(20, 430, anchor="nw")
        self.canvas2.itemconfig(
            self.login1, text="Already have an account", font=(10))
        btn1 = tk.Button(
            self,
            bg="#99b6ff",
            text='Login',
            height=1,
            width=10, command=lambda: controller.show_frame("Login")
        )
        self.canvas2.create_window(240, 440, window=btn1)

    ################ Insert user in DB ################
    def insert_userr(self):
        if(
            self.entry1.get() == "" or
            self.entry2.get() == "" or
            self.entry3.get() == "" or
            self.entry4.get() == ""
        ):
            messagebox.showerror(
                "ERORR", "ALL FIELDS ARE REQUIRED", parent=self.controller)
        else:
            try:
                name = self.entry1.get()
                username = self.entry2.get()
                email = self.entry3.get()
                password = self.entry4.get()
                user = helper.insert_user(name, username, email, password)
                if user == "USER SUCCESSFULLY SAVED":
                    self.controller.show_frame("Login")
                messagebox.showinfo(
                    "Info", user, parent=self.controller)
            except Exception as es:
                messagebox.showerror(
                    "ERORR", f"ERROR DUE TO: {str(es)}", parent=self.controller)

############################################ Login PAGE ############################################
class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ####################### Create 1st canvas #######################
        self.canvas1 = tk.Canvas(
            self,
            bg="#1b1063",
            width=700,
            height=1000
        )
        self.canvas1.place(x=-20, y=-20)

        ####################### Write Welcome text #######################
        self.canvas1.create_text(
            370,
            100,
            text="WELCOME TO STT",
            fill="white",
            font=('Helvetica 15 bold')
        )
        ####################### Put image on 1st canvas #######################
        self.tkimage = ImageTk.PhotoImage(Image.open("1.png"))
        self.canvas1.create_image(
            -230,
            0,
            image=self.tkimage,
            anchor=tk.NW
        )
        ####################### Write Welcome text #######################
        self.canvas1.create_text(
            370,
            100,
            text="Speech To Text With AI",
            fill="white",
            font=('Helvetica 15 bold')
        )
        ####################### Create 2nd canvas #######################
        self.canvas2 = tk.Canvas(
            self,
            bg="white",
            width=700,
            height=1000
        )
        self.canvas2.place(x=680, y=-20)

        ####################### Write Sign up text #######################
        self.canvas2.create_text(
            170,
            100,
            text="Login",
            fill="black",
            font=('Helvetica 15 bold')
        )

        ####################### Email and its field #######################
        self.text_canvas1 = self.canvas2.create_text(60, 190, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas1, text="Email", font=(20))
        self.entry3 = tk.Entry(self)
        self.canvas2.create_window(170, 200, window=self.entry3)

        ####################### Password and its field #######################
        self.text_canvas2 = self.canvas2.create_text(30, 220, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas2, text="Password", font=(20))
        self.entry4 = tk.Entry(self, show="*", width=20)
        self.canvas2.create_window(170, 230, window=self.entry4)

        ####################### Sign up Button #######################
        btn1 = tk.Button(
            self,
            text='Login',
            bg="#99b6ff",
            command = self.login,
            height=1,
            width=10,

        )
        self.canvas2.create_window(170, 350, window=btn1)

        ####################### Drow Line #######################

        self.canvas2.create_line(0, 390, 400, 390)

        ####################### Already have account Login Buuton #######################

        self.login1 = self.canvas2.create_text(20, 430, anchor="nw")
        self.canvas2.itemconfig(
            self.login1, text="Don't have an account", font=(10))
        btn1 = tk.Button(
            self,
            bg="#99b6ff",
            text='Signup',
            height=1,
            width=10, command=lambda: controller.show_frame("Signup")
        )
        self.canvas2.create_window(240, 440, window=btn1)

    def login(self):
        if(
            self.entry3.get() == "" or
            self.entry4.get() == ""
        ):
            messagebox.showerror(
                "ERORR", "ALL FIELDS ARE REQUIRED", parent=self.controller)
        else:
            try:
                email = self.entry3.get()
                password = self.entry4.get()

                fetch = helper.Fetch_by_email(email, password)
                if fetch =="LOGIN SUCCESSFULL":
                    self.controller.show_frame("Dashboard")
                messagebox.showinfo(
                    "Info", fetch, parent=self.controller)
            except Exception as es:
                messagebox.showerror(
                    "ERORR", f"ERROR DUE TO: {str(es)}", parent=self.controller)
    
############################################ Dashboard PAGE ############################################
class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        
        ####################### Put image on 1st canvas #######################
        self.image = ImageTk.PhotoImage(Image.open("dash_img1.jpg"))
        background_label = tk.Label(self, image=self.image)
        background_label.place(x=-20, y=80)
        
        ####################### Create 1st canvas #######################
        self.canvas1 = tk.Canvas(
            self,
            bg="#1b1063",
            width=1100,
            height=100
        )
        self.canvas1.place(x=-20, y=-20)

        ####################### Write Welcome text #######################
        self.canvas1.create_text(
            520,
            60,
            text="WELCOME TO STT",
            fill="white",
            font=('Helvetica 15 bold')
        )

        logout_btn = tk.Button(self, text="Logout", font="20",
                               command=lambda: controller.show_frame("Signup"))
        logout_btn.place(x=900, y=25)

        profile_btn = tk.Button(self, text="Profile", font="20", command=lambda: controller.show_frame("Profile"))
        profile_btn.place(x=30, y=25)
        
        bg_image = tk.Button(
            self,
            text='Choose file and get text',
            command=self.bgImage,
            height=2,
            width=20
        )
        bg_image.place(x=430, y=300)

    def bgImage(self):
        self.path = filedialog.askopenfilename(
            filetypes=(
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            )
        )
        full_text = self.get_large_audio_transcription(self.path)
        messagebox.showinfo(
            "SUCCESS", full_text, parent=self.controller)

    def get_large_audio_transcription(self, path):
        sound = AudioSegment.from_wav(path)
        chunks = split_on_silence(sound,
                                  min_silence_len=500,
                                  silence_thresh=sound.dBFS-14,
                                  keep_silence=500,
                                  )
        folder_name = "audio-chunks"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""

        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text
        return whole_text
        
############################################ Profile PAGE ############################################
class Profile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
    ####################### Create Window #######################
        self.controller .title('Text to speach')
        self.controller.geometry('1000x600')
        self.controller.resizable(0, 0)

        ####################### Create 1st canvas #######################
        """self.canvas1 = tk.Canvas(
            self,
            bg="white",
            width=700,
            height=1000
        )
        self.canvas1.place(x=-20, y=-20)"""

        lable =  tk.Label(self, text="Application Users", font=("time 25 bold"), bg= 'blue')
        lable.grid(row=0, column=0, columnspan=20)
        
        p1 = tk.Label(self, text = "ID", font="time 15 bold")
        p1.grid(row =1 , column=0, padx = 10, pady = 10)
        
        p1 = tk.Label(self, text = "Username", font="time 15 bold")
        p1.grid(row =1 , column=1, padx = 10, pady = 10)
        
        p1 = tk.Label(self, text = "Name", font="time 15 bold")
        p1.grid(row =1 , column=2, padx = 10, pady = 10)
        
        p1 = tk.Label(self, text = "Email", font="time 15 bold")
        p1.grid(row =1 , column=3, padx = 10, pady = 10)
        
        p1 = tk.Label(self, text="Password", font="time 15 bold")
        p1.grid(row=1, column=4, padx=10, pady=10)
        
        num = 2
        fetch_all = helper.Fetch_All()
        for i in fetch_all:
            id = tk.Label(self, text =i[0], font ="time 12 bold", fg = 'blue')
            id.grid(row =num, column=0, padx = 10, pady = 10)

            username = tk.Label(self, text =i[1], font ="time 12 bold", fg = 'blue')
            username.grid(row =num, column=1, padx = 10, pady = 10)
            
            name = tk.Label(self, text =i[2], font ="time 12 bold", fg = 'blue')
            name.grid(row =num, column=2, padx = 10, pady = 10)
            
            email = tk.Label(self, text =i[3], font ="time 12 bold", fg = 'blue')
            email.grid(row =num, column=3, padx = 10, pady = 10)
            
            password = tk.Label(self, text =i[4], font ="time 12 bold", fg = 'blue')
            password.grid(row =num, column=4, padx = 10, pady = 10)
            
            num =num+1
            
        self.canvas2 = tk.Canvas(
            self,
            bg="white",
            width=700,
            height=1000
        )
        self.canvas2.place(x=680, y=-20)
        ####################### Write Sign up text #######################
        self.canvas2.create_text(
            170,
            100,
            text="ADD USER",
            fill="black",
            font=('Helvetica 15 bold')
        )

        ####################### Name and its field #######################
        self.text_canvas1 = self.canvas2.create_text(60, 190, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas1, text="Name", font=(20))
        self.entry1 = tk.Entry(self)
        self.canvas2.create_window(170, 200, window=self.entry1)

        ####################### Username and its field #######################
        self.text_canvas2 = self.canvas2.create_text(30, 220, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas2, text="Username", font=(20))
        self.entry2 = tk.Entry(self)
        self.canvas2.create_window(170, 230, window=self.entry2)

        ####################### Email and its field #######################
        self.text_canvas3 = self.canvas2.create_text(60, 250, anchor="nw")
        self.canvas2.itemconfig(self.text_canvas3, text="Email", font=(20))
        self.entry3 = tk.Entry(self)
        self.canvas2.create_window(170, 260, window=self.entry3)

        ####################### Password and its field #######################
        self.text_canva4 = self.canvas2.create_text(30, 280, anchor="nw")
        self.canvas2.itemconfig(self.text_canva4, text="Password", font=(20))
        self.entry4 = tk.Entry(self, show="*", width=20)
        self.canvas2.create_window(170, 290, window=self.entry4)

        ####################### Sign up Button #######################
        btn1 = tk.Button(
            self,
            text='Signup',
            bg="#99b6ff",
            height=1,
            command=self.insert_userr,
            width=10
        )
        self.canvas2.create_window(170, 350, window=btn1)

        ####################### Drow Line #######################

        self.canvas2.create_line(0, 390, 400, 390)

        ####################### Already have account Login Buuton #######################

        self.login1 = self.canvas2.create_text(20, 430, anchor="nw")
        self.canvas2.itemconfig(
            self.login1, text="Return Dashboard", font=(10))
        btn1 = tk.Button(
            self,
            bg="#99b6ff",
            text='Dashboad',
            height=1,
            width=10, command=lambda: controller.show_frame("Dashboard")
        )
        self.canvas2.create_window(240, 440, window=btn1)

    ################ Insert user in DB ################
    def insert_userr(self):
        if(
            self.entry1.get() == "" or
            self.entry2.get() == "" or
            self.entry3.get() == "" or
            self.entry4.get() == ""
        ):
            messagebox.showerror(
                "ERORR", "ALL FIELDS ARE REQUIRED", parent=self.controller)
        else:
            try:
                name = self.entry1.get()
                username = self.entry2.get()
                email = self.entry3.get()
                password = self.entry4.get()
                user = helper.insert_user(name, username, email, password)
                messagebox.showinfo(
                    "Info", user, parent=self.controller)
            except Exception as es:
                messagebox.showerror(
                    "ERORR", f"ERROR DUE TO: {str(es)}", parent=self.controller)
    
    
    
    
    
if __name__ == "__main__":
    r = sr.Recognizer()
    helper = DBHelper()
    app = Mian()
    app.mainloop()
