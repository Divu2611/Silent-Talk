import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image

from predict import predict

class Applicaion:

    def __init__(self):
        self.root = Tk()

        width= self.root.winfo_screenwidth()
        height= self.root.winfo_screenheight()

        self.root.geometry("%dx%d" % (width, height))
        self.root.title("Silent Talk")

        self.capture = cv.VideoCapture(0)

        self.videoFrame = Label(self.root)
        self.videoFrame.pack(pady=(50,20))

        self.frame = Label(self.root)
        self.frame.pack(pady=(0,30))

        self.voiceButton = Button(self.frame, text="Voice")
        self.voiceButton.grid(row=0, column=0)

        self.clearButton = Button(self.frame, text="Clear")
        self.clearButton.grid(row=0, column=1)

        self.resultPanel = Label(self.root)
        self.resultPanel.place(x = 350, y = 900)

        self.character = str()
        self.charPanel = Label(self.resultPanel)
        self.charTitle = Label(self.charPanel,text="Character :", font=("Arial Black", 40))
        self.charTitle.grid(row=0,column=0)
        self.charPred = Label(self.charPanel)
        self.charPred.grid(row=0,column=1)
        self.charPanel.grid(row=0, column=0, sticky=W)

        self.word = str()
        self.wordPanel = Label(self.resultPanel, text="Word :", font=("Arial Black", 40))
        self.wordPanel.grid(row=1, column=0, sticky=W)

        self.sentence = str()
        self.sentencePanel = Label(self.resultPanel, text="Sentence :", font=("Arial Black", 40))
        self.sentencePanel.grid(row=2, column=0, sticky=W)

        self.openCamera()

    def openCamera(self):

        success,frame = self.capture.read()

        if success:

            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            startPt = list()
            startPt.append(10)
            startPt.append(60)

            endPt = list()
            endPt.append(310)
            endPt.append(360)

            cv.rectangle(frame, tuple(startPt), tuple(endPt), (255,0,0), 4) 

            regionOfInterest = frame[startPt[1]:endPt[1],startPt[0]:endPt[0]]
            sign = Image.fromarray(regionOfInterest)
            sign = sign.resize((300,300))

            frame = Image.fromarray(frame)
            frame = frame.resize((1500,750))
            frameTk = ImageTk.PhotoImage(frame)

            self.videoFrame.configure(image = frameTk)
            self.videoFrame.frameTk = frameTk

            # self.character = predict(sign)
            self.character = 'A'
            self.charPred.configure(text=self.character, font=("Arial", 40))

        else:
            print("Unable to read frames...")

        self.root.after(30, self.openCamera)

    def speakData(self):
        pass

    def clearData(self):
        pass

print("Starting Application...")

app = Applicaion()
app.root.mainloop()