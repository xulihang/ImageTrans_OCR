class Detector:
    def __init__(self,name):
        self.name=name        
        
    def get_name(self):
        return self.name
        
    def detect(self, image):
        """Detect text areas in images."""
        raise NotImplementedError