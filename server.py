#!/usr/bin/env python3

import os
import time
import datetime
import cv2
from imagetrans_ocr import ImageTransOCR
from bottle import route, run, template, request, static_file
import json
from config import *
    
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
    print(recognize_entire_image)
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

    ocr.init_detector(detector_name)
    ocr.init_recognizer(recognizer_name)
    if recognize_entire_image==True:        
        text=ocr.recognize(file_path)
        os.remove(file_path)
        return text
    else:        
        ret=ocr.detect(file_path,skip_recogniztion)
        os.remove(file_path)
        return ret    


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='www')
    
ocr = ImageTransOCR()
run(server="paste",host='0.0.0.0', port=8080)     

