import nltk
import difflib
import string
from string import punctuation
from tkinter import *
import tkinter.messagebox as tm
from PIL import ImageTk, Image
import hashlib
import os
import random
import sys
import nltk.corpus
import time
import nltk.stem.snowball
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from tkinter import messagebox

import utils
from utils import *

import dataPopulate
from dataPopulate import *

passthres = 0.4
conf = utils.get_config()

stops = stopwords.words('english')
stops.extend(string.punctuation)
stops.append('')

stemmer = nltk.stem.snowball.SnowballStemmer('english')
lemmer = nltk.stem.wordnet.WordNetLemmatizer()

Default_Resp = "Sorry, I cannot answer that question. Please stand by for a live rep."
Welcome_Message = ['Good Day, How may I assist?', 'Welcome to the SLB Chat Bot, how may i help you']


def sent_analyzer():
    request = input ('Good day, How may I assist?')
    sentence = sent_tokenize(request)
    words = word_tokenize(request)
    POS = nltk.pos_tag(words)
    keywords = nltk.chunk.ne_chunk(POS)
    return(words)
    print (keywords)
    

def botting(s):
    sent=s.lower()
    hashid=hashing(sent)
    matchrate=parser(sent)
    timestamp=timestamp_string()
    SQL = "SELECT DISTINCT 1 faqid FROM faq WHERE faqid = %s;"
    count=cursor.execute(SQL,(hashid))
    SQL2 = "SELECT DISTINCT 1 hashid FROM faq WHERE rating = %s;"
    count2=cursor.execute(SQL2,(matchrate))
    SQL3 = "INSERT INTO log (timestamp, question,sucess_answer) VALUES (%s, %s, %s);" 
    SQL4 = "SELECT * FROM faq;"
    print(hashid)
    print(matchrate)
    print(count)
    print(count2)
    if(count>0):
        SQL = "SELECT answer FROM faq  WHERE faqid = %s;"
        cursor.execute(SQL,(hashid))
        row=cursor.fetchall() 
        for x in row:
            print(x["answer"])
            success="Yes"
            cursor.execute(SQL3,(timestamp,sent,success))
            return(x["answer"])
                   
    elif(count2>0):
        SQL = "SELECT answer FROM faq WHERE rating = %s;"
        cursor.execute(SQL,(matchrate))
        row=cursor.fetchall()
        for x in row:
            print(x["answer"])
            success="Yes"
            cursor.execute(SQL3,(timestamp,sent,success))
            return(x["answer"])
    elif(count==0):
        cursor.execute(SQL4)
        row=cursor.fetchall()
        for x in row:         
            jack=sent_jacker(sent,x["question"])
            print(sent)
            print(x["question"])
            print(jack)
            if jack == True:
                push=x["answer"]
                SQL6="INSERT INTO faq (faqID,question,answer,rating) VALUES (%s, %s, %s, %s);"
                cursor.execute(SQL6,(hashid,sent,push,matchrate))
                return (push)
                print(x["answer"])
            else:
                #SQL ="INSERT INTO sentence (hashid, questions) VALUES (%s, %s);"
                #cursor.execute(SQL,(hashid,sent))
                success="No"
                cursor.execute(SQL3,(timestamp,sent,success))
                push=Default_Resp
        return(push)
    


def sent_jacker(a,b):
        
        token_b = [token.lower().strip(string.punctuation) for token in word_tokenize(b)
               if token.lower().strip(string.punctuation) not in stops]
        token_a = [token.lower().strip(string.punctuation) for token in word_tokenize(a)
               if token.lower().strip(string.punctuation) not in stops]

        stems_a = [stemmer.stem(token) for token in token_a if len(token) > 0]
        stems_b = [stemmer.stem(token) for token in token_b if len(token) > 0]

        #return (stems_a == stems_b)
        #s = difflib.SequenceMatcher(None, stems_a, stems_b)
        ratio = len(set(stems_a).intersection(stems_b)) / float(len(set(stems_a).union(stems_b)))
        print (ratio)
        return (ratio >= passthres)
    
def hashing(sentence):
    return hashlib.md5(str(sentence).encode('utf-8')).hexdigest()[:16]

def calc_insurance(TRN,ylts):
    SQL = "SELECT amount FROM loans WHERE trn = %s, status = owing;"
    cursor.execute(SQL,(TRN))
    row=cursor.fetchall()
    for x in row:
        amt = x["amount"]
        insurance = ((amt/1000)*0.50)*ylts


def click(event):
    entered_text = textentry.get()
    user ="Me: " + entered_text
    label2 = Label(frame,anchor=W,wraplength=450,background="sky blue",text = user,justify=LEFT)
    label2.pack()

    #while True:
    if entered_text =='' or entered_text.strip(punctuation).lower() == 'quit' or entered_text.strip(punctuation).lower() == 'exit':
        answer=query_yes_no("Are you sure you wish to Quit?")
        if answer:
            answer="Thank You For Using Me"
            close_window()
    answer=botting(entered_text)
    connection.commit()

    bot = "SLBot: " + answer
    label = Label(frame,anchor=W,wraplength=450,background="sky blue", text = bot,justify=LEFT)
    input_user.set('')
    time.sleep(1)
 
    label.pack()


    return "break"


def close_window():
    window.destroy()

def login(event):

    label_username = Label(frame2,text="Username")
    label_password = Label(frame2,text="TRN")

    entry_username = Entry(frame2)
    entry_password = Entry(frame2,show="*")

    label_username.pack()
    entry_username.pack()
    label_password.pack()
    entry_password.pack()

    checkbox = Checkbutton(frame2,text="Keep me logged in")
    checkbox.pack()

    logbtn = Button(frame2,text="Login")
    logbtn.pack()
    logbtn.bind('<Button-1>',_login_btn_clicked)
    exlog = Button(frame2,text="Close")
    exlog.pack()
    exlog.bind('<Button-1>',login_destroy)
    frame2.pack(side=BOTTOM, fill=X)

def _login_btn_clicked(event):
    # print("Clicked")
    username = entry_username.get()
    password = entry_password.get()
    SQL7 = "INSERT INTO user(userID,username) VALUES (%s,%s)"
    cursor.execute(SQL7,(password,username))
    # print(username, password)

    if username == True and password == True:
        tm.showinfo("Login info", "Welcome"+entry_username)

def login_destroy(event):
    frame2.destroy()
    


#onve code is launched connect to database and open UI
if __name__ == "__main__":

    
    configr = utils.get_config()


    DBHOST = configr["MySQL"]["server"]
    DBUSER = configr["MySQL"]["dbuser"]
    DBNAME = configr["MySQL"]["dbname"]

    print("Starting Bot...")
    print("Connecting to database...")
    connection = utils.db_connection(DBHOST, DBUSER, DBNAME)
    cursor = connection.cursor()
    connectionID = utils.db_connectionID(cursor)
    print(".... CONNECTED ....")
    
    welcometext=random.choice(Welcome_Message)

    #chat window
    window= Tk()
    window.title("SLB-Bot")
    #login()
    bar = Scrollbar(window)
    bar.pack(side=RIGHT, fill=Y)

    #img = ImageTk.PhotoImage(Image.open("slbot.png"))
    #panel = Label(root, image = img)
    #panel.pack(side = "bottom", fill = "both", expand = "no")
    wel_msg = Label(window,background="sky blue",text=welcometext, font=("Arial Bold",18))
    wel_msg.pack()
    
    input_user = StringVar()
    textentry = Entry(window, text=input_user)
    textentry.pack(side=BOTTOM, fill=X)
    
    frame = Frame(window, width=500, height=1000)
    frame.configure(background="sky blue")
    frame.pack_propagate(False) # prevent frame to resize to the labels size
    textentry.bind("<Return>", click)
    frame.pack(side=TOP, fill=BOTH)
    frame2 = Frame(frame, width=500, height=25)
    
    feedback_button = Button(frame,text="Give Feedback")
    feedback_button.pack(side=TOP, fill=X)
    login_button = Button(frame,text="Login")
    login_button.pack(side=TOP, fill=X)
    login_button.bind('<Button-1>',login)
    
    frame.config(yscrollcommand=bar.set)
    bar.config(command=frame.yview)
    
    #run mainloop
    window.mainloop()
        


        
    
    
