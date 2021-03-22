import numpy as np

def get_polygon_from_rect(x,y,width,height):
    box={}
    box["x0"]=x
    box["y0"]=y
    box["x1"]=x+width
    box["y1"]=y
    box["x2"]=x+width
    box["y2"]=y+height
    box["x3"]=x
    box["y3"]=y+height
    box["text"]=""
    return box    

def convert_boxes_array_to_textlines(boxes_array):
    textlines=[]
    for result in boxes_array:
        line={}
        index=0
        for coord in result:
            line["x"+str(index)]=int(coord[0])
            line["y"+str(index)]=int(coord[1])
            index=index+1
        line["text"]=""
        textlines.append(line)
    return textlines
    
def convert_textlines_to_boxes_array(textlines):
    boxes_array=[]
    for line in textlines:
        points=[]
        for i in range(4):
            points.append([line["x"+str(i)],line["y"+str(i)]])
        boxes_array.append(np.array(points, dtype = "int16"))
    return boxes_array

def convert_textline_to_rect(textline):
    minx=textline["x0"]
    maxx=0
    miny=textline["y0"]
    maxy=0
    rect={}
    for i in range(0,4):
        minx=min(minx,textline["x"+str(i)])
        maxx=max(maxx,textline["x"+str(i)])
        miny=min(miny,textline["y"+str(i)])
        maxy=max(maxy,textline["y"+str(i)])
    rect["x"]=minx
    rect["y"]=miny
    rect["width"]=maxx-minx
    rect["height"]=maxy-miny
    rect["text"]=textline["text"]
    return rect
    
def convert_words_to_textlines(words):
    words.sort(key=lambda x:x["x0"],reverse=False) #sort boxes based on left
    # To be done
    
def overlapped_percent(box1,box2,horizontal):
    x1=box1["x"]
    y1=box1["y"]
    w1=box1["width"]
    h1=box1["height"]
    maxx1=x1+w1
    maxy1=y1+h1
    x2=box2["x"]
    y2=box2["y"]
    w2=box2["width"]
    h2=box2["height"]
    maxx2=x2+w2
    maxy2=y2+h2
    percent=0
    if horizontal:
        if (maxy1-y2)>=0 and (y2>=y1):
            percent=(maxy1-y2)/min(h1,h2)
        elif (maxy2-y1)>=0 and (y1>=y2):
            percent=(maxy2-y1)/min(h1,h2)
    else:
        if (maxx1-x2)>=0 and (x2>=x1):
            percent=(maxx1-x2)/min(w1,w2)
        elif (maxx2-x1)>=0 and (x1>=x2):
            percent=(maxx2-x1)/min(w1,w2)
    return percent