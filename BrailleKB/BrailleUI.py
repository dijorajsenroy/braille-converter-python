import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import braille as braille
import threading
import pyaudio
import wave

import speech_recognition as sr
##Recorder App
class App():
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
    fs = 44100  
    
    frames = []  
    def __init__(self, main):
        self.isrecording = False
        self.button1 = tk.Button(main, text='rec',command=self.startrecording)
        self.button2 = tk.Button(main, text='stop',command=self.stoprecording)
        self.button1.pack()
        self.button2.pack()
    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()
    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename=input('the filename?')
        self.filename = self.filename+".wav"
        r = sr.Recognizer()
        hellow=sr.AudioFile(self.filename)
        with hellow as source:
            audio = r.record(source)
        try:
            s = r.recognize_google(audio)
            print("Text equivalent of Speech: "+s)
        except Exception as e:
            print("Exception: "+str(e))
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
    def record(self):
       while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
		

##text conversion Window
def textconv():
    win1 = tk.Tk()
    win1.geometry("600x300")
    win1.title("Text Conversion")
    l1 =tk.Label(win1, text="English to Braille")
    l2 =tk.Label(win1, text="Braille to English")
    e1 = tk.Entry(win1)
    e2 = tk.Entry(win1)
    l1.grid(row=1)
    l2.grid(row=2)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    def op(): 
        print("The braille equivalent of the given is:\n")
        s1 = str(e1.get())
        eb1=braille.textToBraille(s1)
        eb2=braille.brailleToTextArray(e2.get())
        print(eb1)
    b = tk.Button(win1, text = "Get output", command=op)
    b.configure(width=20,height=6)
    b.grid(row=3, column=1)
    win1.mainloop()

##speech conversion window
def speechconv():
    win2 = tk.Tk()
    win2.geometry("100x100")
    win2.title("Speech Conversion")
    app = App(win2)
    win2.mainloop()
##image conversion window:
def imgconv():
    win3 = tk.Tk()
    win3.geometry("600x300")
    win3.title("Image conversion")
    tk.Label(win3,text="Enter Image Path:").grid(row=1)
    e = tk.Entry(win3)
    e.grid(row=1,column=1)
    def con():
        path = str(e.get())
        print(braille.imagetoBraille(path))
    sub = tk.Button(win3, text = "Submmit for Output",command=con)
    sub.configure(width=20,height=6)
    sub.grid(row=2,column=1)
    win3.mainloop()
## Main Window
root = tk.Tk()
root.geometry("900x1000")
root.title("Braille Keyboard App")
img_t = Image.open("/Users/dijorajsenroy/code_files/brailleKB/braille.png")
img_t4= img_t.resize((600, 500), Image.ANTIALIAS)
img4 = ImageTk.PhotoImage(img_t4)
panel = tk.Label(root, image = img4)
panel.pack(side = "top")
but1 = tk.Button(root, text = "Text to Braille/Braille to Text Conversion",command =textconv)
but1.configure(width=15,height=6)
but2 = tk.Button(root, text = "Speech to Braille/Braille to Speech Conversion",  command =speechconv)
but2.configure(width=15,height=6)
but3 = tk.Button(root, text = "Image to Braille/Braille to Image Conversion", command = imgconv)
but3.configure(width=15,height=6)
but1.pack(side="bottom",fill=X)
but2.pack(side="bottom",fill=X)
but3.pack(side="bottom",fill=X)
root.mainloop()