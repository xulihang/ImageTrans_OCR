class ImageTransOCR():

    def __init__(self):
        self.detector = None
        self.recognizer= None
        
    def detect(self,file_path,skip_recogniztion=False):
        boxes=[]
        boxes = self.detector.detect(file_path)
        if skip_recogniztion==False:
            self.recognizer.recognize(file_path,boxes,False)
        ret={}
        ret["boxes"]=boxes
        return ret
    
    def recognize(self,file_path):
        boxes=[]
        text=self.recognizer.recognize(file_path,boxes,True)
        return text        
    
    def init_detector(self,name):
        if self.detector!=None:
            if self.detector.name==name:        
                return
        if name=="craft" or name==None:
            from craft_detector import CRAFTDetector
            self.detector = CRAFTDetector(name)
        elif name=="chineseocr":
            from chineseocr_detector import ChineseOCRDetector
            self.detector = ChineseOCRDetector(name)
        
    def init_recognizer(self,name):
        if self.recognizer!=None:
            if self.recognizer.name==name:        
                return
        if name=="opencv" or name==None:
            from opencv_recognizer import OpenCVRecognizer
            self.recognizer = OpenCVRecognizer(name)
        elif name=="chineseocr":
            from chineseocr_recognizer import ChineseOCRRecognizer
            self.recognizer = ChineseOCRRecognizer(name)