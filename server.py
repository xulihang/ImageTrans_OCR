#!/usr/bin/env python3

import os
import time
import datetime
import cv2
from bottle import route, run, template, request, static_file
import json
import keras_ocr
from craft_detector import CRAFTDetector
from opencv_recognizer import OpenCVRecognizer
    
@route('/ocr', method='POST')
def ocr():
    upload = request.files.get('upload')   
    recognize_entire_image = request.forms.get('recognize_entire_image')    
    skip_recogniztion = request.forms.get('skip_recogniztion')
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
    words=[]
    if recognize_entire_image==True:        
        text=recognizer.recognize(file_path,words,recognize_entire_image)
        os.remove(file_path)
        return text
    else:        
        words = detector.detect(file_path)
        if skip_recogniztion==False:
            recognizer= OpenCVRecognizer("crnn_cs_CN.onnx","alphabet_3944.txt")
            recognizer.recognize(file_path,words,False)
        ret={}
        ret["words"]=words
        os.remove(file_path)
        return ret    


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='www')
    
detector = CRAFTDetector()
recognizer= OpenCVRecognizer("crnn_cs_CN.onnx","alphabet_3944.txt")
run(server="paste",host='127.0.0.1', port=8080)     

