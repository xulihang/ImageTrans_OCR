import numpy as np
import cv2 as cv
import math
from recognizer import Recognizer
from config import *
import utils

class OpenCVRecognizer(Recognizer):

    def __init__(self,name):
        self.vocabulary=self.readVocabulary(opencv_alphabet)
        self.net=cv.dnn.readNetFromONNX(opencv_model)
        self.name=name
    
    def recognize(self, image, words, recognize_entire_image):
        img = cv.imread(image)
        if recognize_entire_image==False:
            for word in words:
                rect=utils.convert_textline_to_rect(word)
                x=rect["x"]
                y=rect["y"]
                width=rect["width"]
                height=rect["height"]
                cropped = img[y:y+height, x:x+width]
                word["text"]=self.recognizeOneClip(cropped)
        else:        
            return self.recognizeOneClip(img)
        
    def recognizeOneClip(self,img):        
        # if use padding
        # img = fill_img(img, inpWidth, inpHeight)
        blob = cv.dnn.blobFromImage(img, size=(100, 32), mean=127.5, scalefactor=1 / 255.0)
        blob -= 0.5
        blob /= 0.5
        self.net.setInput(blob)
        # Run the recognition model
        result = self.net.forward()
        # decode the result into text
        wordRecognized = self.decodeText(result)
        print("recog output is : ", wordRecognized)
        return wordRecognized
        
    def decodeText(self, scores):
        text = ""
        for i in range(scores.shape[0]):
            c = np.argmax(scores[i][0])
            print(c)
            if c != 0:
                text += self.vocabulary[c - 1]
            else:
                text += '-'

        # adjacent same letters as well as background text must be removed to get the final output
        print(text)
        char_list = []
        for i in range(len(text)):
            if text[i] != '-' and (not (i > 0 and text[i] == text[i - 1])):
                char_list.append(text[i])
        return ''.join(char_list)

    def readVocabulary(self,vocabularyPath):
        vocabulary=[]
        f = open(vocabularyPath, 'r',encoding="utf-8")
        for line in f.readlines():
            character=line.replace("\n","").replace("\r","")
            vocabulary.append(character)
        return vocabulary    
