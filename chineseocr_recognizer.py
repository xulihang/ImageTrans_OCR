#coding=utf-8
from chineseocr_lite.crnn import CRNNHandle
from chineseocr_lite.angnet import  AngleNetHandle
from chineseocr_lite.utils import sorted_boxes, get_rotate_crop_image
from chineseocr_lite.dbnet.dbnet_infer import DBNET
from chineseocr_config import *
from recognizer import Recognizer
from PIL import Image
from utils import convert_textlines_to_boxes_array
import numpy as np
import cv2
import copy
import traceback

class ChineseOCRRecognizer(Recognizer):

    def __init__(self,name):
        self.crnn_handle = CRNNHandle(crnn_model_path)
        self.name = name;
        if angle_detect:
            self.angle_handle = AngleNetHandle(angle_net_path)
        
    def recognize(self,image, boxes_list, recognize_entire_image):
        results = self.crnnRecWithBox(np.array(Image.open(image)), convert_textlines_to_boxes_array(boxes_list))
        print(results)

        newBoxes=[]
        for result in results:
            #box=boxes_list[index]
            #box["text"]=result[1]
            newBox={}
            index=0           
            for coord in result[0]:
                newBox["x"+str(index)]=int(coord[0])
                newBox["y"+str(index)]=int(coord[1])
                index=index+1
            newBox["text"]=result[1]
            newBoxes.append(newBox)
        boxes_list.clear()
        boxes_list.extend(newBoxes)
    
    def crnnRecWithBox(self,im, boxes_list):
        """
        crnn模型，ocr识别
        @@model,
        @@converter,
        @@im:Array
        @@text_recs:text box
        @@ifIm:是否输出box对应的img

        """
        results = []
        line_imgs = []

        for index, (box) in enumerate(boxes_list[:angle_detect_num]):
            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))
            partImg = Image.fromarray(partImg_array).convert("RGB")
            line_imgs.append(partImg)

        angle_res = False
        if angle_detect:
            angle_res = self.angle_handle.predict_rbgs(line_imgs)

        count = 1
        for index, (box) in enumerate(boxes_list):

            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))


            partImg = Image.fromarray(partImg_array).convert("RGB")

            if angle_detect and angle_res:
                partImg = partImg.rotate(180)


            if not is_rgb:
                partImg = partImg.convert('L')

            try:
                if is_rgb:
                    simPred = self.crnn_handle.predict_rbg(partImg)  ##识别的文本
                else:
                    simPred = self.crnn_handle.predict(partImg)  ##识别的文本
            except Exception as e:
                print(traceback.format_exc())
                continue

            if simPred.strip() != '':
                results.append([tmp_box, simPred])
                count += 1

        return results
