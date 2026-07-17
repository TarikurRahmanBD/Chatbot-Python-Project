import re
import pickle
import numpy as np
import json
import random

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

try:
    from keras.models import load_model
    model = load_model('chatbot_model.h5')
except Exception:
    model = None


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array using a simple regex fallback
    sentence_words = re.findall(r"\w+", sentence.lower())
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    if model is None:
        return []
    try:
        # filter out predictions below a threshold
        p = bow(sentence, words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list
    except Exception:
        return []


def getResponse(ints, intents_json):
    if not ints:
        tag = "noanswer"
    else:
        tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


def get_fallback_response(msg):
    text = msg.lower()
    if any(word in text for word in ["hi", "hello", "hey", "hola"]):
        return "Hello! How can I help you today?"
    if any(word in text for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Come back again soon."
    if any(word in text for word in ["thanks", "thank you"]):
        return "You're welcome!"
    if any(word in text for word in ["are you ai", "ai", "bot", "chatbot"]):
        return "Yes, I am a chatbot here to help with basic medical support questions."
    if any(word in text for word in ["who created you", "created you", "your creator", "who made you"]):
        return "I was created by Tariqur Rahman Sir. You can see his work here: https://github.com/tarikurrahmanbd"
    if any(word in text for word in ["what can you do", "what do you do", "help me", "can you help"]):
        return "I can help with greetings, basic medical support, blood pressure, pharmacy, hospital, and drug-related questions."
    if any(word in text for word in ["what is your name", "your name", "who are you"]):
        return "I'm your friendly chatbot assistant."
    if any(word in text for word in ["how old are you", "your age"]):
        return "I don't have a real age, but I’m here to help you right now."
    if any(word in text for word in ["where are you from", "where do you live"]):
        return "I live in this chat and I’m available whenever you need help."
    if any(word in text for word in ["are you helpful", "helpful", "useful"]):
        return "Yes, I’m here to help with simple questions and support."
    if any(word in text for word in ["what is your purpose", "your purpose", "purpose"]):
        return "My purpose is to assist you with friendly conversations and basic support questions."
    if any(word in text for word in ["can you speak bangla", "speak bangla", "bangla"]):
        return "Yes, I can respond in Bangla too."
    if any(word in text for word in ["what is this project", "what is this chatbot", "about this project", "project name"]):
        return "This project is a Python chatbot built for basic conversation and medical-support-style responses."
    if any(word in text for word in ["what technology", "which language", "built with", "used python", "python"]):
        return "This project is built using Python with Tkinter for the interface and simple NLP-based response handling."
    if any(word in text for word in ["what is the topic", "topic", "project topic"]):
        return "The project topic is a chatbot application for interactive support and conversation."
    if any(word in text for word in ["blood pressure", "pressure"]):
        return "I can help with blood pressure tracking."
    if any(word in text for word in ["pharmacy", "drug", "adverse"]):
        return "I can help with pharmacy and adverse drug information."
    if any(word in text for word in ["hospital"]):
        return "I can help with hospital searches."
    if any(word in text for word in ["help", "support", "option"]):
        return "I can guide you through medical support options."
    return "Sorry, I can help with greetings, goodbye, thanks, blood pressure, pharmacies, hospitals, and drug information."


def chatbot_response(msg):
    ints = predict_class(msg, model)
    if ints:
        return getResponse(ints, intents)
    return get_fallback_response(msg)


#Creating GUI with tkinter
import tkinter
from tkinter import *


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

def create_gui():
    global base, ChatLog, EntryBox, SendButton

    base = Tk()
    base.title("Hello")
    base.geometry("400x500")
    base.resizable(width=FALSE, height=FALSE)

    #Create Chat window
    ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

    ChatLog.config(state=DISABLED)

    #Bind scrollbar to Chat window
    scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set

    #Create Button to send message
    SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                        command=send)

    #Create the box to enter message
    EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
    #EntryBox.bind("<Return>", send)


    #Place all components on the screen
    scrollbar.place(x=376,y=6, height=386)
    ChatLog.place(x=6,y=6, height=386, width=370)
    EntryBox.place(x=128, y=401, height=90, width=265)
    SendButton.place(x=6, y=401, height=90)


def run_console_chat():
    print("Chatbot started. Type 'quit' to exit.")
    while True:
        try:
            message = input("You: ").strip()
        except EOFError:
            break
        if not message:
            continue
        if message.lower() in {"quit", "exit"}:
            print("Bot: Goodbye!")
            break
        print("Bot:", chatbot_response(message))


if __name__ == "__main__":
    try:
        create_gui()
        base.mainloop()
    except Exception:
        run_console_chat()
