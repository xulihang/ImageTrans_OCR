import keras_ocr
from detector import Detector

class CRAFTDetector(Detector):

    def __init__(self):
        self.detector = keras_ocr.detection.Detector()
        
    def detect(self, image):
        
        images = [keras_ocr.tools.read(image)]
        box_groups = self.detector.detect(images=images)
        prediction=box_groups[0]
        text_lines=[]
        for result in prediction:
            line={}
            index=0
            for coord in result:
                line["x"+str(index)]=int(coord[0])
                line["y"+str(index)]=int(coord[1])
                index=index+1
            line["text"]=""
            text_lines.append(line)
        return text_lines