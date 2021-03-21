import keras_ocr
from utils import convert_boxes_array_to_textlines
from detector import Detector

class CRAFTDetector(Detector):

    def __init__(self,name):
        self.detector = keras_ocr.detection.Detector()
        self.name=name
        
    def detect(self, image):        
        images = [keras_ocr.tools.read(image)]
        box_groups = self.detector.detect(images=images)
        prediction=box_groups[0]
        return convert_boxes_array_to_textlines(prediction)
