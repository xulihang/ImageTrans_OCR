import keras_ocr
from detector import Detector

class CRAFTDetector(Detector):

    def __init__(self):
        self.pipeline = keras_ocr.pipeline.Pipeline()
        
    def detect(self, image):
        
        images = [keras_ocr.tools.read(image)]
        prediction_groups = self.pipeline.recognize(images,do_recognition=False)
        prediction=prediction_groups[0]
        text_lines=[]
        print(prediction)

        for result in prediction:
            line={}
            index=0
            for coord in result[1]:
                line["x"+str(index)]=int(coord[0])
                line["y"+str(index)]=int(coord[1])
                index=index+1
            line["text"]=result[0]
            text_lines.append(line)
        return text_lines