api_key = "AIzaSyBjG8gyTzjsSGRHeal62CfIET4mo7AcVk8"
client_id = '688177377737-m6afvklpmuu494dc1ra9rk83g7mgvpsb.apps.googleusercontent.com'
secret = 'FsFVXRQ_W0j6fMIszcFwTcRw'
client_secret_file = 'client_secret_688177377737-m6afvklpmuu494dc1ra9rk83g7mgvpsb.apps.googleusercontent.com.json'
scopes = ['https://www.googleapis.com/auth/youtube']

import os
import json
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from sentiment_analysis import main as analyse_sentiment
from creating_image import main as generate_image
flow = InstalledAppFlow.from_client_secrets_file(client_secret_file,scopes)
credentials = flow.run_console()
youtube = build('youtube','v3', developerKey=api_key)
youtube2 = build('youtube','v3',credentials=credentials)
from googleapiclient.http import MediaFileUpload
import cv2
import urllib
import numpy as np
import time
#Get Channel ID

def get_img_from_url(url):
    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def collect_comments(Id_file='my_vid_id.txt'):
    
    with open(Id_file,'r') as f:
        video_ids = f.readlines()    

    #videos = video_ids[0:10]
    for initial_video in video_ids[0:1]:
        next_page_token = None
        i = 0
        existing_list = {}
        
        while True:
            req = youtube.commentThreads().list(part = 'snippet',videoId=initial_video,maxResults=1,pageToken=next_page_token).execute()        
            if req['items'][0]['snippet']['topLevelComment']['id'] in existing_list:
                req = youtube.commentThreads().list(part = 'snippet',videoId=initial_video,maxResults=1,pageToken=None).execute()

            comment = req['items'][0]['snippet']['topLevelComment']['snippet']['textOriginal']
            emotions_values,sentiment,total,total_emotion,word_count = analyse_sentiment(comment,'no')
            commentor = req['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName']
            commentor_img = get_img_from_url(req['items'][0]['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
            
            next_page_token = req.get('nextPageToken')
            print(comment)
            if next_page_token is None or req['items'][0]['snippet']['topLevelComment']['id'] in existing_list:
                bot = cv2.imread('bot.png')
                img = cv2.imread('surreal.png')
                img[670:720,320:960] = (255,255,255)
                img[671:719,360:408] = bot
                font = cv2.FONT_HERSHEY_SIMPLEX
                img = cv2.putText(img,'feed me with a comment',(450,705),font,1,(0,0,0),2,cv2.LINE_AA)
                cv2.imwrite(f'Images/{i}.jpg',img)
                youtube2.thumbnails().set(videoId=initial_video,media_body=MediaFileUpload(f'Images/{i}.jpg')).execute()     
                i += 1
            else:
                img = generate_image(word_count,sentiment,total,total_emotion,emotions_values,commentor,commentor_img)
                cv2.imwrite(f'Images/{i}.jpg',img)
                youtube2.thumbnails().set(videoId=initial_video,media_body=MediaFileUpload(f'Images/{i}.jpg')).execute()     
                i += 1       
            existing_list[req['items'][0]['snippet']['topLevelComment']['id']] = 'exists'    
            time.sleep(60*10)
            
#[items][0]['snippet']
#Tom_scott_channel_ID = 'UCBa659QWEk1AI4Tg--mrJ2A'
#video_Ids = get_youtube_videos_ID(Tom_scott_channel_ID)
#print(len(video_Ids))
collect_comments()


def get_channel_ID(name='shubh patni',part='snippet',type='channel'):

    channel_ID = youtube.search().list(q=name,part=part,type=type)
    Id = channel_ID.execute()
    channels = {}
    for item in Id['items']:
        channels[item['snippet']['title']] = {'ID':item['snippet']['channelId'],'description':item['snippet']['description']}
    return channels

#print(get_channel_ID())

#Get ALL VIDEO ID'

def get_youtube_videos_ID(id):
    channel_details = youtube.channels().list(id=id,part='contentDetails').execute()
    playlist_ID = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None
    
    while True:
        video_dtls = youtube.playlistItems().list(playlistId=playlist_ID,part='snippet',maxResults=1,pageToken=next_page_token).execute()
        videos += video_dtls['items'][0]['snippet']['resourceId']['videoId']
        with open('Tom_scott_videos.txt','a') as f:
            f.write(video_dtls['items'][0]['snippet']['resourceId']['videoId'] + '\n')

        next_page_token = video_dtls.get('nextPageToken')
        if next_page_token is None:
            break
    
    return videos

"""else:
        data = json.load('my_vid_comments.json')
        if data.get(req['items'][0]['snippet']['topLevelComment']['id']) is None:
            dictionary = {req['items'][0]['snippet']['topLevelComment']['id']:req['items'][0]['snippet']['topLevelComment']['snippet']['textOriginal']}
            f.dump(dictionary,f)"""


 