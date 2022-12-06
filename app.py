## Importing Libraries
import cv2 as cv

from tkinter import *
from PIL import ImageTk, Image

from string import ascii_uppercase

import pyttsx3

from predict import predict

## Creating an Application class
class Applicaion:

    def __init__(self):
        self.root = Tk()

        width= self.root.winfo_screenwidth()
        height= self.root.winfo_screenheight()

        ## Setting the title bar
        self.root.geometry("%dx%d" % (width, height))
        self.root.title("Silent Talk")
        self.root.iconphoto(False, PhotoImage(file='Icons/favicon.png'))

        self.capture = cv.VideoCapture(0)

        self.videoFrame = Label(self.root)
        self.videoFrame.pack(pady=(50,20))

        self.frame = Label(self.root)
        self.frame.pack(pady=(0,30))

        self.prediction = False
        self.predicted = False

        ## Start button to start the predictions
        self.startButton = Button(self.frame, text="Start", command=self.startPrediction, width=10, height=2, bg="#14A44D", fg="white", font="Arial 15 bold")
        self.startButton.grid(row=0, column=0, padx=20)

        ## Stop button to stop the predictions
        self.stopButton = Button(self.frame, text="Stop", command=self.stopPrediction, state=DISABLED, width=10, height=2, bg="#DC4C64", fg="white", font="Arial 15 bold")
        self.stopButton.grid(row=0, column=1, padx=20)

        ## Voice button to speak the data
        self.voiceButton = Button(self.frame, text="Voice", command=self.speakData, state=DISABLED, width=10, height=2, bg="#54B4D3", fg="white", font="Arial 15 bold")
        self.voiceButton.grid(row=0, column=2, padx=20)

        ## Clear button to clear the data
        self.clearButton = Button(self.frame, text="Clear", command=self.clearData, state=DISABLED, width=10, height=2, bg="#E4A11B", fg="white", font="Arial 15 bold")
        self.clearButton.grid(row=0, column=3, padx=20)

        self.titles = Label(self.root)
        self.titles.place(x = 350, y = 900)

        self.charTitle = Label(self.titles,text="Character :", font=("Arial Black", 40))
        self.charTitle.grid(row=0,column=0,sticky=W)
        self.wordTitle = Label(self.titles,text="Word :", font=("Arial Black", 40))
        self.wordTitle.grid(row=1,column=0, sticky=W)
        self.sentenceTitle = Label(self.titles,text="Sentence :", font=("Arial Black", 40))
        self.sentenceTitle.grid(row=2,column=0, sticky=W)

        self.resultPanel = Label(self.root)
        self.resultPanel.place(x = 750, y = 900)

        self.count = dict()
        self.reset()

        ## Panel for character predicted
        self.character = str()
        self.charPred = Label(self.resultPanel)
        self.charPred.grid(row=0,column=0,sticky=W)

        ## Panel for word predicted
        self.word = str()
        self.wordPred = Label(self.resultPanel)
        self.wordPred.grid(row=1,column=0,sticky=W)

        ## Panel for sentence predicted
        self.sentence = str()
        self.sentencePred = Label(self.resultPanel)
        self.sentencePred.grid(row=2,column=0,sticky=W)

        self.openCamera()

    def openCamera(self):

        success,frame = self.capture.read()

        if success: ## Capturing Frames

            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            startPt = list()
            startPt.append(10)
            startPt.append(60)

            endPt = list()
            endPt.append(310)
            endPt.append(360)

            ## Creating region of interests where signs are to be shown
            cv.rectangle(frame, tuple(startPt), tuple(endPt), (255,0,0), 4) 

            ## Converting region of interest from numpy array to Image
            regionOfInterest = frame[startPt[1]:endPt[1],startPt[0]:endPt[0]]
            sign = Image.fromarray(regionOfInterest)
            sign = sign.resize((300,300))

            frame = Image.fromarray(frame)
            frame = frame.resize((1500,750))
            frameTk = ImageTk.PhotoImage(frame)

            self.videoFrame.configure(image = frameTk)
            self.videoFrame.frameTk = frameTk

            if self.prediction: ## Only if start button is pressed

                self.makePrediction(sign)

                if self.character == 'nothing': ## Updating predicted character
                    self.charPred.configure(text="-", font=("Arial", 50))
                else:
                    self.charPred.configure(text=self.character, font=("Arial", 50))

                self.wordPred.configure(text=self.word, font=("Arial", 50)) ## Updating predicted word
                self.sentencePred.configure(text=self.sentence, font=("Arial", 50)) ## Updating predicted sentence

        else:
            print("Unable to read frames...")

        self.root.after(30, self.openCamera)

    def startPrediction(self):
        ## Start button is pressed and prediction started
        self.prediction = True

        self.startButton.configure(state= DISABLED)
        self.stopButton['state'] = 'normal'
        self.clearButton['state'] = 'normal'

    def makePrediction(self, sign):
        ## Making prediction
        self.character = predict(sign)

        self.count[self.character] += 1
        if self.count[self.character] >= 20: ## A character is considered to be predicted only if it is found in 20 or more frames 
            if self.character in ascii_uppercase:
                self.word += self.character ## If character is an alphabet then it is appended to the word
            elif self.character == 'del':
                self.word = self.word[:-1] ## If character is 'del' then last letter of current word is deleted
            elif self.character == 'space':
                self.sentence += self.word + " " ## If character is 'space' then word is considered to be predicted and is appended to sentence
                self.word = ""

            self.reset() ## After a character is predicted it gets reset and the cycle goes on

    def stopPrediction(self):
        ## Stop button is pressed and prediction stopped
        self.prediction = False
        self.predicted = True

        self.startButton['state'] = 'normal'
        self.stopButton.configure(state= DISABLED)
        self.voiceButton['state'] = 'normal'

    def speakData(self):
        ## Voice assistant feature to convert final predicted output to speech
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 125)

        engine.say(self.sentence)
        engine.runAndWait()

    def clearData(self):
        ## Clearing the data
        self.reset()

        self.character = ""
        self.word = ""
        self.sentence = ""

    def reset(self):
        self.count['del'] = 0
        self.count['nothing'] = 0
        self.count['space'] = 0
        
        for i in ascii_uppercase:
            self.count[i] = 0

        for i in range(10):
            self.count[i] = 0

print("Starting Application...")

app = Applicaion()
app.root.mainloop()