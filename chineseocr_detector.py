from utils import convert_boxes_array_to_textlines
from chineseocr_lite.dbnet.dbnet_infer import DBNET
from chineseocr_lite.utils import sorted_boxes
from detector import Detector
from chineseocr_config import *
from PIL import Image
import numpy as np

class ChineseOCRDetector(Detector):

    def __init__(self,name):
        self.text_handle = DBNET(model_path)
        self.name = name
        
    def detect(self,img_path,short_size=960):
        img=Image.open(img_path)
        try:
            if hasattr(img, '_getexif') and img._getexif() is not None:
                orientation = 274
                exif = dict(img._getexif().items())
                if orientation not in exif:
                    exif[orientation] = 0
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
        except Exception as ex:
            pass
        
        if img.width<200 and img.height<200:
            short_size=196
        short_size = 32 * (short_size//32)        
        img = img.convert("RGB")
        
        boxes_list, score_list = self.text_handle.process(np.asarray(img).astype(np.uint8), short_size=int(short_size))         
        boxes_list = sorted_boxes(np.array(boxes_list))        
        return convert_boxes_array_to_textlines(boxes_list)
