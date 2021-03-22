from chineseocr_config import *
from chineseocr_lite.angnet import AngleNetHandle
from PIL import Image

class AngleDetector():

    def __init__(self):
        self.angle_handle = AngleNetHandle(angle_net_path)
        
    def rotate_if_neccessary(self,img):
        pred=self.angle_handle.predict_rbg(img)
        print(pred)
        if pred>0.5:
            img = img.rotate(180)
            return img
        else:
            return img
            
            
if __name__=="__main__":
    detector=AngleDetector()
    detector.rotate_if_neccessary(Image.open("1616386965264.jpg").convert("RGB"))