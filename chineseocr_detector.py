from utils import convert_boxes_array_to_textlines
from chineseocr_lite.dbnet.dbnet_infer import DBNET
from chineseocr_lite.utils import sorted_boxes
from detector import Detector
from chineseocr_config import *
from PIL import Image
import numpy as np

class ChineseOCRDetector(Detector):

    def __init__(self):
        self.text_handle = DBNET(model_path)
        
    def detect(self,img,short_size=960):
        img=Image.open(img)
        boxes_list, score_list = self.text_handle.process(np.asarray(img).astype(np.uint8),short_size=short_size)           
        boxes_list = sorted_boxes(np.array(boxes_list))        
        return convert_boxes_array_to_textlines(boxes_list)
