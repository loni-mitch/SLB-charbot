import nltk
import string
from string import punctuation
from tkinter import *
import hashlib
import os
import random
import sys
import nltk.corpus
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import utils
from utils import *

conf = utils.get_config()

DBHOST = conf["MySQL"]["server"]
DBUSER = conf["MySQL"]["dbuser"]
DBNAME = conf["MySQL"]["dbname"]

connection = utils.db_connection(DBHOST, DBUSER, DBNAME)
cursor = connection.cursor()
connectionID = utils.db_connectionID(cursor)
    
def hashing(sentence):
    return hashlib.md5(str(sentence).encode('utf-8')).hexdigest()[:16]

def parser(s):
    sent=s.lower()
    words = word_tokenize(sent)
    FilterW = words
    rating = 0
    for i in words:
        if i in stops:
            FilterW.remove(i)
    pos = nltk.pos_tag(FilterW)
    for each in pos:
        print(pos)
        tag = each[1]
        print(tag)
        SQL="SELECT rating FROM nltktags WHERE tag = %s;"
        cursor.execute(SQL,(tag))
        tg=cursor.fetchall()
        for x in tg:
            rating = rating + x["rating"]
    return str(rating)
        
def data_populate():

    file = open("faqs.txt", "r")
    lines = file.readlines()
    file.close()
    file2 = open("ans.txt", "r")
    ansline = file2.readlines()
    file2.close()
    count = len(open("faqs.txt").readlines())
    count2 = len(open("ans.txt").readlines())
    print(count)
    print(count2)
    while (count != 0):
        b=lines[count-1].lower()
        x=ansline[count-1]
        rate=parser(b)
        print(b)
        print(b.strip('\n'))
        hashid=hashing((b.strip(' \n')).lower())
        SQL ="INSERT INTO faq (faqID,question,answer,rating) VALUES (%s, %s, %s, %s);"
        cursor.execute(SQL,(hashid,b,x,rate))
        count=count-1
        print(count)
        connection.commit()
   
