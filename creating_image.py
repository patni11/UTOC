#Creating_image
import numpy as np
import cv2
import random
from itertools import chain
import emoji as emoticon

'''
Min is 2 max is 20
                                            comments  anger  anticipation  disgust  fear  joy  negative  positive  sadness  surprise  trust  total
1  Some years ago I was involved in a Land Rover ...      1             3        0     0    1         1         4        1         0      3     14

negative: 1
positive: 4
total: 14
total_emotion: 9
{'anger': 1, 'anticipation': 3, 'disgust': 0, 'fear': 0, 'joy': 1, 'sadness': 1, 'surprise': 0, 'trust': 3}

'''

def get_rgb(weighted_random_emotion_picker,sentiment):

    emotions_color = {'anger':(181,7,37),'anticipation':(242,86,30),'disgust': (60,3,59),'fear': (83,149,24),'joy':(231,210,46),'sadness': (19,125,213),'surprise':(16,127,42),'trust':(156,182,35)}
    
    emotion = random.choice(weighted_random_emotion_picker)
    r,g,b = emotions_color[emotion]
    
    r += random.randint(0,sentiment['negative'] * 10)
    if r > 255.0:
        r = 255
    b += random.randint(0,sentiment['positive'] * 10)
    if b > 255.0:
        b = 255
    return r,g,b

def convert_to_bgr(r,g,b):
    return (b,g,r)

def generate_img(height,width,size,weighted_random_emotion_picker,sentiment):
    img = np.ones([height,width,3])
    for i in range(0,height,size):
        for j in range(0,width,size):
            r,g,b = get_rgb(weighted_random_emotion_picker,sentiment)
            b,g,r = convert_to_bgr(r,g,b)
            img[i:i+size,j:j+size,0] = b/255.0
            img[i:i+size,j:j+size,1] = g/255.0
            img[i:i+size,j:j+size,2] = r/255.0

    return img


def create_horizontal_Img(l_path):
    images = []
    for each in l_path:
        images.append(cv2.imread(each))
    img_h = cv2.hconcat(images)
    return img_h,len(l_path)

def main(word_count,sentiment,total,total_emotion,emotion_values,commentor,commentor_img):
    size = 100-word_count
    emotions_emoji = {'anger': 'Emojis/anger.png', 'anticipation': 'Emojis/shh.png', 'disgust': 'Emojis/disgust.png', 'fear': 'Emojis/fear.png', 'joy': 'Emojis/laugh.png', 'sadness': 'Emojis/crying.png', 'surprise': 'Emojis/surprise.png', 'trust': 'Emojis/trust.png'}
    if size<4:
        size = random.randint(4,10)
    elif  size > 20:
        size = random.randint(10,20)    

    for each in list(emotion_values.keys()):
        if emotion_values[each] < 1:
            emotion_values.pop(each)

    weighted_random_emotion_picker = [[keys]*emotion_values[keys] for keys in emotion_values.keys()]
    weighted_random_emotion_picker = list(chain.from_iterable(weighted_random_emotion_picker))  
    
    emojis = [emotions_emoji[keys] for keys in emotion_values]    
    emoji_img,length = create_horizontal_Img(emojis)
    
    if weighted_random_emotion_picker :
        img = generate_img(720,1280,size,weighted_random_emotion_picker,sentiment)
        img = img*255
        img[670:720,320:960] = (255,255,255)
        img[671:719,360:408] = commentor_img
        end = 420+(48*length)
        img[671:719,420:end] = emoji_img
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        img = cv2.putText(img,commentor,(end+10,700),font,1,(0,0,0),2,cv2.LINE_AA)
    else:
        img = cv2.imread('glitch.png')
        img[670:720,320:960] = (255,255,255)
        img[671:719,360:408] = commentor_img
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.putText(img,commentor,(450,705),font,1,(0,0,0),2,cv2.LINE_AA)
        
    return img    