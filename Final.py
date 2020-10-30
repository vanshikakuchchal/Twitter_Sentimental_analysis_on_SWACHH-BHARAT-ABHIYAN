from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize
import nltk
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
def clean(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9_+]+|(\w+:\/\/\S+))|(#[A-Za-z0-9_+]+)|(&amp)|(http[A-Za-z0-9_+]+)", " ", tweet).split())
def cleanpunc(tweet):
    return ' '.join(re.sub("([-`,/])|([_'! * ?:%&;|¦~<>=])", " ", tweet).split())
def correctdot(tweet):
    return ' '.join(re.sub("([.])", ". ", tweet).split())

def lexiconrate(s):
        score = analyser.polarity_scores(s)
        # if(score['compound']>0):
        #     score['compound']=0.8*score['compound']
        return score['compound']
    
def bigramapproach(text):
    senti=0
    count=0
    for i in text:
        pos=nltk.pos_tag(i)
        if((pos[0][1]=='RB' or pos[0][1]=='RBR' or pos[0][1]=='RBS') and (pos[1][1]=='JJ' or pos[1][1]=='JJR' or pos[1][1]=='JJS')):
            s1=pos[0][0]+" "+pos[1][0]
            senti=senti+lexiconrate(s1)
            count=count+1
        if(pos[0][1]=='JJ' or pos[0][1]=='JJR' or pos[0][1]=='JJS' or pos[1][1]=='JJ' or pos[1][1]=='JJR' or pos[1][1]=='JJS'):
            s2=pos[0][0]+" "+pos[1][0]
            senti=senti+lexiconrate(s2)
            count=count+1
    if(count==0):
        return senti
    else:
        return (senti/count)

def getsentiment(text):
    sentencetokenize=sent_tokenize(text)
    senti = 0
    for i in sentencetokenize:
        wordstokenize=word_tokenize(i.lower())
        wordstokenize=list(ngrams(wordstokenize, 2))
        senti = senti + bigramapproach(wordstokenize)
    return senti

neg=pos=0
n=p=0
with open('final_tweet_data.csv', mode='r') as csv_file:
    csv_reader=csv.reader(csv_file)
    for row in csv_reader:
        tweet=str(row)
        text=clean("".join(tweet))
        text=cleanpunc(text)
        text=correctdot(text)
        senti = getsentiment(text)
        if(senti>=0.05):
                p=p+1
                pos=pos+senti
                print(tweet,"In Favour with a score of ",senti)
        if(senti<0.00):
                n=n+1 
                neg=neg+senti
                print(tweet,"Against with a score of ",senti)
try:
    print("\n\n\n\nAverage In Favour")
    positive=(pos/p)*100
    print(positive,"percent")
except ZeroDivisionError:
    print("0")
try:
    print("\nAverage Against")
    negative=(-neg/n)*100
    print(negative,"percent")
except ZeroDivisionError:
    print("0")
print("\nAverage Neutral ")
print(100-positive-negative,"percent")
successrate=(positive/(positive+negative))*100
print("\n\nSucess Rate of Swachh Bharat Mission Will be ",successrate,"percent")
csv_file.close()