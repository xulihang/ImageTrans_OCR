class Recognizer:
    def __init__(self,name):
        self.name=name
        
    def get_name(self):
        return self.name
        
    def recognize(self, image, boxes):
        """Recognize text from images using a list of bounding boxes."""
        raise NotImplementedError
