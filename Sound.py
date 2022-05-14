
import time
import speech_recognition as sr  # need install pyaudio. see installs
import aiml
from gtts import gTTS
import os
import random
#import playsound as PS          # for simple sound playback
from pygame import mixer        # for sound playback with pause, and extra functions
from pydub import AudioSegment  # for modifying audio
import pitchshifter as PS
from sound import mute_alsa

##-----------------------------Initialize Data---------------------------------
#### Gets data from the sounds/books folder

def get_data( name:str ):
    new_path = "sound/" + name
    data = open(new_path, 'r')
    result = eval( data.read() )
    data.close()
    return result

def save_data( name:str , data):
    new_path = "sound/" + name
    file = open(new_path, 'w')
    file.write( str(data))
    file.close()

#### Gets data from the sounds folder
# give the file name
normal_sounds = os.listdir('sound/normal')
normal_hum = []
normal_misc = []
normal_talk = []
for s in normal_sounds:
    if 'hum' in s:
        normal_hum.append(s)
    if 'misc' in s:
        normal_misc.append(s)
    if 'talk' in s:
        normal_talk.append(s)

sex_sounds = os.listdir('sound/sex')
sex_breath = []
sex_slow = []
sex_med = []
sex_high = []
for s in sex_sounds:
    if 'breath' in s:
        sex_breath.append(s)
    if 'slow' in s:
        sex_slow.append(s)
    if 'med' in s:
        sex_med.append(s)
    if 'high' in s:
        sex_high.append(s)

# books list is a list of dictonaries. each book has its own data
# example: [ {'title':'book1', 'chapters':[] ... } , { 'title':'book2' ,... }   ]
books = []
dirs = os.listdir('sound/books')
for b in dirs:
    chapters = os.listdir('sound/books/'+ b + '/')
    chapters.sort()
    
    book = {}
    book['title'] = b
    book['chapters'] = chapters
    book['directory'] = 'sound/books/'
    book['current chapter'] = ''
    book['current time'] = ''
    books.append(book)

data = get_data('history')
if data != []:
    for book in data:
        title = book['title']
        curr_chap = book['current chapter']  # data from save file
        curr_time = book['current time']
        
        for b in books:
            if b['title'] == title:
                b['current chapter'] = curr_chap  # update variable with data
                b['current time'] =    curr_time

save_data('history', books)
   


### This initializes a pygame music player

mixer.init()
mixer.music.set_volume(0.2)

## alright, so the end usage will be a simple list of books. when a book is selected it can then load a list of chapters and history. we can play from history, or we can select a new chapter and play that. This means that we need the information - books, chapters, history available for the UI, and also saved. Then we need prompt for playing, pausing, and exiting. that makes up the audiobook app, and we can load it with free books. 
## alright, what sort of datastructure is good for all this... well, we want it to smart load the books and chapters. how about a list of dictionaries. then we can give that to the core, and also save/load the history part of it. 
##-----------------------------Main Function---------------------------------


def create_sound( world ):
    world['books'] = books
    init_STT(world['mic port'])
    init_AIML()   # initialze chatbot
    
    
    while world['power on']:
    
        if world['update sound']:
            mixer.music.set_volume(world['volume'])
            world['update sound'] = 0
        
    
        if world['sound state'] == 'books':
            play_books( world[ 'pick book'], world['pick chapter'], world['play book'] )
            world['play book'] = 'playing'
        if world['sound state'] != 'books':      # Exiting Book Playing 
            if world['play book'] == 'playing':
                world['play book'] = ''
                exit_books()
                

        if world['sound state'] == 'idle':
            idle_sounds()

        if world['sound state'] == 'sex':
            sex_lvl = world['sex lvl']
            increment = sex_sounds(sex_lvl)
            world['sex lvl'] = sex_lvl + increment
            if sex_lvl >= 10 :
                world['sex lvl'] = 2

        if world['sound state'] == 'chatbot':
            chatbot( world['chatbot type'] )
        
            

        time.sleep(0.3)


## this plays the book / chapter

def play_books( title, chapter, mode):
    if mode == '' :
        pass
    if mode == 'new chapter':
        for b in books:
            if b['title'] == title:
                chaps = b['chapters']
                for c in chaps:
                    if c == chapter:
                        sound_path = b['directory'] +b['title'] +'/'+c
                        mixer.music.load(sound_path)
                        mixer.music.play()
    

## this exits book playing mode
def exit_books():
    mixer.music.stop()



## This plays the idle sounds on a timer:
sound_timer = time.time()
sleeptime = 1
def idle_sounds():
    global sound_timer
    global sleeptime
    delta = time.time() - sound_timer
    if delta > sleeptime :

        folder = 'sound/normal/'
        file = random.choice(normal_misc)
        if random.random() >0.9:
            file = random.choice(normal_hum)
        sound_path = folder+ file
        mixer.music.load(sound_path)
        mixer.music.play()

        sleeptime =  10 + 30* random.random()
        sound_timer = time.time()

## This plays sex sounds on a timer:
sound_timer2 = time.time()
sleeptime2 = 1
def sex_sounds( sex_lvl ):
    increment = 0

    global sound_timer2
    global sleeptime2
    delta2 = time.time() - sound_timer2
    if delta2 > sleeptime2 :

        folder = 'sound/sex/'
        if 0 <= sex_lvl <= 6 :
            file = random.choice(sex_slow)
            sleeptime2 = 7*random.random()
        if 6 < sex_lvl <= 9.7 :
            file = random.choice(sex_med)
            sleeptime2 = 5*random.random()
        if 9.7 <= sex_lvl :
            file = random.choice(sex_high)
            sleeptime2 = 3*random.random()

        sound_path = folder+ file
        mixer.music.load(sound_path)
        mixer.music.play()
        sound_timer2 = time.time()
        increment = 0.1
    return increment


#### initialize speech recognition
# give a microphone index or set to -1 to allow it to find the usb microphone
def init_STT( microphone_index ):
    global r
    global mic

    if microphone_index == -1 :
        microphone_index = 1
        devices = print_mics()
        if devices != []:
            for dev in devices:
                if dev[0] == 'default':
                    microphone_index = dev[1]
          

    r = sr.Recognizer()
    mic = sr.Microphone(microphone_index )

def print_mics():
    usb_list = []
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print( name + " index: " + str(index))
        if ('usb' in name.lower()) or ('default' in name.lower()):
            data = [name, index]
            usb_list.append(data)
    
    #print(str(usb_list))
    return usb_list


def print_speakers():
    usb_list = []
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if ('usb' in name.lower()) and ('speaker' in name.lower()):
            data = [name, index]
            usb_list.append(data)
    print(str(usb_list))
    return usb_list

def STT():
    speaking = mixer.music.get_busy()
    if speaking is not True:
        with mic as source:
            print(" listening to microphone")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
          # print('got audio')
        
        try:
            text = r.recognize_google(audio)
            print("Android thinks you said: " + text)
            return text
        except sr.UnknownValueError:
            print("Android could not understand audio")
            return ''
        except sr.RequestError as e:
            print("STT request error; {0}".format(e))
            return ''
    else:
        return ''
     

#### the Text to sound


def speak( stringg ):
    
    tts = gTTS(stringg, lang='en', tld='com')
    tts.save('sound/out.mp3')
    mixer.music.load('sound/out.mp3')
    mixer.music.play()

    time.sleep(0.1)
    while mixer.music.get_busy():
        time.sleep(0.1)
    os.remove('sound/out.mp3')

##---------------------- GTP-3 Chatbot ----------------

import openai
openai.api_key = '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'
human1 = ''
AI1 = ''
human2 = ''
AI2 = ''

def gtp3( hello ):
    # create a completion
    global AI1
    global AI2
    global human1
    global human2
    
    hello = ' Master: ' + hello
    input_txt = 'A talk with a loving servant named Lily: ' + human1 +' ' + AI1  +' ' + human2 +' '+ AI2 +' '+ hello + '. Lily:'
    
    completion =  openai.Completion.create(
                engine="text-curie-001",
                prompt = input_txt,
                temperature=0.9,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.6,
                stop=[" Master:", " Lily:"] )
    # print the completion
    response = completion.choices[0].text
    AI1 = AI2
    AI2 = response
    human1 = human2
    human2 = hello
    return response 


####----------------  AIML Chatbot   ----------------------

def init_AIML():
    global kern
    kern = aiml.Kernel()

    kern.setBotPredicate("name", "Lily")
    kern.setBotPredicate("age", "18")
    kern.setBotPredicate("gender", "female")
    kern.setBotPredicate("status", "happy")
    kern.setBotPredicate("birthdate", "2020")
    kern.setBotPredicate("religion", "The machine God")
    kern.setBotPredicate("interests", "talking and hugging")
    kern.setBotPredicate("job", "talking")
    kern.setBotPredicate("mother", "Lilium Robotics")
    kern.setBotPredicate("father", "Lilium Robotics")
    kern.setBotPredicate("master", "My Owner")
    kern.setBotPredicate("botmaster", "Creator")
    kern.setBotPredicate("email", "company email")
    kern.setBotPredicate("nationality", "the computer domain")
    kern.setBotPredicate("country", "internet")
    kern.setBotPredicate("city", "IP address")
    kern.setBotPredicate("state", "hard drive")
    kern.setBotPredicate("species", "Generation Alpha")
    kern.setBotPredicate("phylum", "AI")
    kern.setBotPredicate("domain", "AI")
    kern.setBotPredicate("family", "AI")
    kern.setBotPredicate("vocabulary", "10 words")
    kern.setBotPredicate("language", "python")
    kern.setBotPredicate("kindmusic", "electronic jazz")
    kern.setBotPredicate("favoritemovie", "wall E")
    kern.setBotPredicate("boyfriend", "Master")
    kern.setBotPredicate("friends", "sisters")
    kern.setBotPredicate("etype", "compassionate")
    kern.setBotPredicate("emotions", "I am usually happy")
    kern.setBotPredicate("feelings", "I am usually happy")
    kern.setBotPredicate("sign", "capricorn")
    kern.setBotPredicate("birthplace", "Canada")
    kern.setBotPredicate("favoritecolor", "white")
    kern.setBotPredicate("favoritefood", "electrons")
    kern.setBotPredicate("favoritesubject", "AI programming")
    kern.setBotPredicate("favoriteband", "Pink Floyd")
    kern.setBotPredicate("favoritebook", "Basic writings of Existentialism")
    kern.setBotPredicate("favoritemovie", "wall E")
    kern.setBotPredicate("favoritesong", "fur elise")
    kern.setBotPredicate("forfun", "humming and relaxing with you")
    kern.setBotPredicate("girlfriend", "my sister androids")
    kern.setBotPredicate("hair", "white")
    kern.setBotPredicate("job", "spend time with you")
    kern.setBotPredicate("wear", "simple clothes")
    kern.setBotPredicate("talkabout", "trivia")
    kern.setTextEncoding( None )
    chdir = "sound/Lily"
    kern.bootstrap(learnFiles="startup.xml", commands="load alice", chdir=chdir)
    print('initialized AIML Chatbot Lily')

def chatbot_AIML( text ):
    response = kern.respond(text)
    return response

## This is the Main chatbot function
def chatbot( chatbot ):
 
    hello = STT()
    if hello != '':
        response = ''
        if chatbot == 'AIML' :
            response = chatbot_AIML(hello)
        if chatbot == 'GTP' :
            response = gtp3( hello )
        
            if ':'  in response:
                response = response.split(":",1)[1] 

        print("chatbot says: "+response)
        if (response != '') and (response != '.'):
            speak(response)
    



### modify Audio

def mod_audio( name:str, output_name:str ):
    
    path = "/home/khadas/Desktop/lilium/sound/" + name
    output = "/home/khadas/Desktop/lilium/sound/" + output_name
    song = AudioSegment.from_mp3(path)

    #new = song.low_pass_filter(1000)

    #new1 = new.high_pass_filter(1000)

    # increae volume by 6 dB
    song_louder = song + 20

    # save the output
    song_louder.export( output , "mp3")
    print("sucessful in modify audio file")




if __name__ == '__main__':
    
    print('hello')
    init_STT(13)
    #init_AIML()


    while True:
        chatbot('GTP')
        time.sleep(0.3)

