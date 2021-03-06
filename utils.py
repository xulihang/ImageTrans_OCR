def convert_points_of_word_to_box(textline):
    minx=textline["x0"]
    maxx=0
    miny=textline["y0"]
    maxy=0
    box={}
    for i in range(0,4):
        minx=min(minx,textline["x"+str(i)])
        maxx=max(maxx,textline["x"+str(i)])
        miny=min(miny,textline["y"+str(i)])
        maxy=max(maxy,textline["y"+str(i)])
    box["x"]=minx
    box["y"]=miny
    box["width"]=maxx-minx
    box["height"]=maxy-miny
    box["text"]=textline["text"]
    return box
    
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