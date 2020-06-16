import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
plt.style.use('classic')
import re
import fileinput
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize 
import nltk

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from tqdm import tqdm as tqdm
from tqdm import trange


def extract_emotion(df,column):
    new_df = df.copy()
    Lexicon = 'NRC-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt' #path to lexicon file
    
    lex_df = pd.read_csv(Lexicon,names=["word", "emotion", "association"],sep='\t') # creates column names as word, emotion and association
    lex_words = lex_df.pivot(index='word',
                                columns='emotion',
                                values='association').reset_index()   #creates 10 extra columns for each emotion

    emotions = lex_words.columns.drop('word')
    emo_df = pd.DataFrame(0, index = new_df.index,columns=emotions)
    #print(emo_df.head())
    total_df = pd.DataFrame(0,index=new_df.index,columns=['total'])
    stemmer = SnowballStemmer('english')

    with tqdm(total=len(list(new_df.iterrows()))) as pbar:
        for i,rows in new_df.iterrows():
            pbar.update(1)
            long_text = word_tokenize(new_df.loc[i][column])
            for word in long_text:
                word = stemmer.stem(word.lower())
                score = lex_words[lex_words.word == word]
                if not score.empty:
                    for emotion in list(emotions):
                        emo_df.at[i, emotion] += score[emotion]
            
            total = emo_df.sum(axis=1,skipna = True)[i]
            total_df.at[i,'total'] = total

    new_df = pd.concat([new_df,emo_df],axis=1)
    new_df = pd.concat([new_df,total_df],axis = 1)
    return new_df                    

def clean_data(df):
    new_df = df.iloc[0]
    emotions_values = {'anger':0,'anticipation':0,'disgust': 0,'fear': 0,'joy':0,'sadness': 0,'surprise':0,'trust':0}
    sentiment = {'negative':new_df['negative'],'positive': new_df['positive']}
    for key in emotions_values.keys():
        emotions_values[key] = new_df[key]
    total = new_df['total']   
    total_emotion = total - (new_df['negative']+ new_df['positive'])
    word_count = new_df['word_count']
    return emotions_values,sentiment,total,total_emotion,word_count

def main(comment,file='yes'):
    if file=='yes':
        with open('my_vid_comments.txt','r') as f:
            comments = f.readlines()
    else:
        comments = [comment+'\n']
    df = pd.DataFrame({'comments':comments})      
    
    new_df = extract_emotion(df,'comments')  
    
    new_df['word_count'] = new_df['comments'].apply(word_tokenize).apply(len)
    emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']
    
    ev,s,t,te,wc = clean_data(new_df)
    '''
    for emotion in emotions:
        new_df[emotion] = new_df[emotion] / new_df['word_count']
    '''
    return ev,s,t,te,wc

