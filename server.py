#!/usr/bin/env python3

import os
import time
import datetime
import cv2
from bottle import route, run, template, request, static_file
import json
    
@route('/ocr', method='POST')
def ocr():
    upload = request.files.get('upload')   
    recognize_entire_image = request.forms.get('recognize_entire_image')    
    skip_recogniztion = request.forms.get('skip_recogniztion')
    detector_name = request.forms.get('detector')
    recognizer_name = request.forms.get('recognizer')
    lang = request.forms.get('lang')
    if recognize_entire_image=="true":
        recognize_entire_image=True
    else:
        recognize_entire_image=False
    if skip_recogniztion=="true":
        skip_recogniztion=True
    else:
        skip_recogniztion=False
        
    name, ext = os.path.splitext(upload.filename)
    print(ext.lower())
    if ext.lower() not in ('.png','.jpg','.jpeg'):
        return "File extension not allowed."
    timestamp=str(int(time.time()*1000))
    savedName=timestamp+ext
    save_path = "./uploaded/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=savedName)
    if os.path.exists(file_path)==True:
        os.remove(file_path)
    upload.save(file_path)    

    init_detector(detector_name)
    init_recognizer(recognizer_name)
    
    boxes=[]
    if recognize_entire_image==True:        
        text=recognizer.recognize(file_path,boxes,recognize_entire_image)
        os.remove(file_path)
        return text
    else:        
        boxes = detector.detect(file_path)
        if skip_recogniztion==False:
            recognizer.recognize(file_path,boxes,False)
        ret={}
        ret["boxes"]=boxes
        os.remove(file_path)
        return ret    


def init_detector(name):
    print(name)
    global detector
    if name=="craft" or name==None:
        from craft_detector import CRAFTDetector
        detector = CRAFTDetector()
    elif name=="chineseocr":
        from chineseocr_detector import ChineseOCRDetector
        detector = ChineseOCRDetector()
        
def init_recognizer(name):
    global recognizer
    if name=="opencv" or name==None:
        from opencv_recognizer import OpenCVRecognizer
        recognizer = OpenCVRecognizer("./model/crnn_cs.onnx","./model/alphabet_94.txt")
    elif name=="chineseocr":
        from chineseocr_recognizer import ChineseOCRRecognizer
        recognizer = ChineseOCRRecognizer()

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='www')
    
detector = None
recognizer= None
run(server="paste",host='0.0.0.0', port=8080)     

