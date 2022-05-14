



## ------------------- Bluetooth section ------------------

import serial
import sys
import time

# this code reads the bluetooth module attached to serial port ttyS3

# If the bluetooth is a module connected to serial port ttyS3 then
# this initializes the port
def init_port():
    uart_channel = serial.Serial("/dev/ttyS3", baudrate=9600, timeout=2)


# reads the serial and returns the data within the buffer time
# returns either the serial data as string or empty string
data = ''
def read_blue():
    global data
    data = uart_channel.readline( 10 ).decode()
    data = str(data)
    return data
    uart_channel.flush()


def data_received(data):
    print(data)
    s.send(data)

## ------------------- Web API Section ------------------

chapters = ''
from flask import Flask, redirect, session, request

def create_API(world):
   
    
    #  Initialize the Book Data
    books = ''

    if world['books'] != []:
        for b in world['books']:
            title = b['title']
            html = '<option>' + title +'</option>'
            books = books + html
    
    
    #import openssl   # need install for ssl to work

    app = Flask(__name__)
    app.config["DEBUG"] = False  # debug causes hot reloads and fucks with system time. 
    app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
    #server = app.config['SERVER_NAME'] = 'lilium.app'
    
    
    
    @app.route("/", methods=['GET', 'POST'])
    def index():
        global chapters
        if request.method == 'POST':
           ##---------------------------------------------- Overall Status Buttons
            if request.form.get('button') == 'Sleep':            
                world['overall state'] = 'sleep'
                world['motion state']  = 'relax'
                world['sound state']   = 'sleep'
                world['vision state']  = 'sleep'
            elif  request.form.get('button') == 'Wake Up':            
                world['overall state'] = 'awake'
                world['motion state']  = 'relax'
                world['sound state']   = 'idle'
                world['vision state']  = 'idle'
            elif  request.form.get('button') == 'Shutdown':        
                world['overall state'] = 'shutdown'
                world['power on'] = 0
              
            
            ##---------------------------------------------- Motion Buttons
            elif request.form.get('buttonM') == 'Relax':      
                world['motion state'] = 'relax'
            elif  request.form.get('buttonM') == 'Lay Back':          
                world['motion state'] = 'lay1'
            elif  request.form.get('buttonM') == 'Floor Sit':           
                world['motion state'] = 'sit1'
            elif request.form.get('buttonM') == 'Curl':             
                world['motion state'] = 'curl'
            elif  request.form.get('buttonM') == '...':
                world['motion state'] = 'relax'
            elif  request.form.get('buttonM') == 'Stiff Spine':           
                if world['stiff spine'] == 1:
                    world['stiff spine'] = 0
                else:
                    world['stiff spine'] = 1
            ##---------------------------------------------- Sex Buttons
            elif request.form.get('buttonS') == 'Relax':      
                world['motion state'] = 'relax'
                world['sound state']  = 'sex'
            elif  request.form.get('buttonS') == 'Missionary':          
                world['motion state'] = 'missionary'
                world['sound state']  = 'sex'
            elif  request.form.get('buttonS') == 'Frontal':           
                world['motion state'] = 'frontal'
                world['sound state']  = 'sex'
            elif request.form.get('buttonS') == 'Doggy':             
                world['motion state'] = 'doggy'
                world['sound state']  = 'sex'
            elif  request.form.get('buttonS') == 'Oral':
                world['motion state'] = 'oral'
                world['sound state']  = 'sex'
            elif  request.form.get('buttonS') == 'Off':           
                world['motion state'] = 'relax'
                world['sound state']  = 'idle'
            ##---------------------------------------------- Sound Buttons
            elif request.form.get('buttonSO') == 'Idle':      
                world['sound state'] = 'idle'
            elif  request.form.get('buttonSO') == 'Chatbot':          
                world['sound state'] = 'chatbot'
            elif  request.form.get('buttonSO') == 'Pick Book':  
                world['sound state'] = 'books' 
                chapters = ''
                try:
                    selected_book = request.form['books']        
                    print(selected_book)
                    world['pick book'] = selected_book
                    for b in world['books']:
                        if b['title'] == selected_book:
                            chapters_s = b['chapters']
                            for c in chapters_s:
                                html = '<option>' + c +'</option>'
                                chapters = chapters + html
                except:
                    print('no books found')
                    
            elif  request.form.get('buttonSO') == 'Pick Chapter':   
                try:
                    selected_chap = request.form['chapter']        
                    print(selected_chap)
                    world['pick chapter'] = selected_chap
                    world['play book'] = 'new chapter'
                except:
                    print('no chapters found')
                
            elif  request.form.get('buttonSO') == 'Volume +':          
                world['volume'] = world['volume'] * 1.3
                world['update sound'] = 1
            elif  request.form.get('buttonSO') == 'Volume -':           
                world['volume'] = world['volume'] * 0.7
                world['update sound'] = 1
                ##---------------------------------------------- Vision Buttons
            elif request.form.get('buttonV') == 'Idle':      
                world['vision state'] = 'idle'
            elif  request.form.get('buttonV') == 'Track Face':          
                world['vision state'] = 'face'
            elif  request.form.get('buttonV') == 'Track Objects':           
                world['vision state'] = 'objects'
 
        ## we have one website page and this is presented here as a big HTML string
                
        return '''<center><h1>Lilium Control App<h1/> 
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <p style="font-size:50%;">Overall State: '''+ world['overall state']+ '''</p>
        <form method="post" action="/">
            <input type="submit" value="Sleep" name="button" style="height:50px; width:100px"/>
            <input type="submit" value="Wake Up" name="button" style="height:50px; width:100px" />
            <input type="submit" value="Shutdown" name="button" style="height:50px; width:100px" />
        </form>
        
        <p style="font-size:50%;">Motion State: '''+ world['motion state']+ '''</p>
        <form method="post" action="/">
            <input type="submit" value="Relax" name="buttonM" style="height:50px; width:100px"/>
            <input type="submit" value="Lay Back" name="buttonM" style="height:50px; width:100px" />
            <input type="submit" value="Floor Sit" name="buttonM" style="height:50px; width:100px" />
        </form>
        <form method="post" action="/">
            <input type="submit" value="Curl" name="buttonM" style="height:50px; width:100px"/>
            <input type="submit" value="..." name="buttonM" style="height:50px; width:100px" />
            <input type="submit" value="Stiff Torso" name="buttonM" style="height:50px; width:100px" />
        </form>
        
        <p style="font-size:50%;">Sex Options</p>
        <form method="post" action="/">
            <input type="submit" value="Relax" name="buttonS" style="height:50px; width:100px"/>
            <input type="submit" value="Missionary" name="buttonS" style="height:50px; width:100px" />
            <input type="submit" value="Frontal" name="buttonS" style="height:50px; width:100px" />
        </form>
        <form method="post" action="/">
            <input type="submit" value="Doggy" name="buttonS" style="height:50px; width:100px"/>
            <input type="submit" value="Oral" name="buttonS" style="height:50px; width:100px" />
            <input type="submit" value="Off" name="buttonS" style="height:50px; width:100px" />
        </form>
        <p style="font-size:50%;">Sound State: '''+ world['sound state']+ '''</p>
        <form method="post" action="/">
            <input type="submit" value="Idle" name="buttonSO" style="height:50px; width:100px"/>
            <input type="submit" value="Chatbot" name="buttonSO" style="height:50px; width:100px" />
        </form>
        <form method="post" action="/">
            <input type="submit" value="Volume +" name="buttonSO" style="height:50px; width:100px"/>
            <input type="submit" value="Volume -" name="buttonSO" style="height:50px; width:100px" />
        </form>
        <p style="font-size:50%;">Book: '''+ world['pick book']+ ''' | Chapter: '''+ world['pick chapter']+ '''</p>
        <form method="post" action="/">
            <label for="books" style="font-size:50%;">Books:</label>
            <select id="books" name="books">
              ''' + books + '''
            </select>
            <input type="submit" value="Pick Book" name="buttonSO" style="height:30px; width:100px" />
        </form>
        <form method="post" action="/">
            <label for="chapter" style="font-size:50%;">Chapters:</label>
            <select id="chapter" name="chapter">
              ''' + chapters + '''
            </select>
            <input type="submit" value="Pick Chapter" name="buttonSO" style="height:30px; width:100px" />
        </form>
 
        <p style="font-size:50%;">Vision State: '''+ world['vision state']+ '''</p>
        <form method="post" action="/">
            <input type="submit" value="Idle" name="buttonV" style="height:50px; width:100px"/>
            <input type="submit" value="Track Face" name="buttonV" style="height:50px; width:100px" />
            <input type="submit" value="Track Objects" name="buttonV" style="height:50px; width:100px" />
        </form>
        
         <center/>''' 
         
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')


### ---------------------- PyQT   GUI ---------------
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Window(QMainWindow):

    def __init__(self, W):
        super().__init__()
        self.setWindowTitle("Lilium")
        self.setGeometry(100, 100, 600, 1300)
        self.statusBar().showMessage('Message in statusbar.')
        self.W = W

        self.button = QPushButton("Relax Mode", self)
        self.button.setGeometry(200, 50, 200, 60)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.click1)
        self.button.setStyleSheet("background-color : lightgrey")

        self.button2 = QPushButton("Lay Down", self)
        self.button2.setGeometry(200, 150, 200, 60)
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.click2)
        self.button2.setStyleSheet("background-color : lightgrey")

        self.button3 = QPushButton("Sit", self)
        self.button3.setGeometry(200, 250, 200, 60)
        self.button3.setCheckable(True)
        self.button3.clicked.connect(self.click3)
        self.button3.setStyleSheet("background-color : lightgrey")

        self.button4 = QPushButton("Sex Relaxed Mode", self)
        self.button4.setGeometry(200, 350, 200, 60)
        self.button4.setCheckable(True)
        self.button4.clicked.connect(self.click4)
        self.button4.setStyleSheet("background-color : lightgrey")

        self.button5 = QPushButton("Sex Missionary", self)
        self.button5.setGeometry(200, 450, 200, 60)
        self.button5.setCheckable(True)
        self.button5.clicked.connect(self.click5)
        self.button5.setStyleSheet("background-color : lightgrey")

        self.button6 = QPushButton("Sex Doggy", self)
        self.button6.setGeometry(200, 550, 200, 60)
        self.button6.setCheckable(True)
        self.button6.clicked.connect(self.click6)
        self.button6.setStyleSheet("background-color : lightgrey")

        self.buttonE = QPushButton("Exit", self)
        self.buttonE.setGeometry(200, 650, 200, 60)
        self.buttonE.setCheckable(True)
        self.buttonE.clicked.connect(self.clickE)
        self.buttonE.setStyleSheet("background-color : lightgrey")

        self.buttonF = QPushButton("Curl", self)
        self.buttonF.setGeometry(200, 750, 200, 60)
        self.buttonF.setCheckable(True)
        self.buttonF.clicked.connect(self.click_curl)
        self.buttonF.setStyleSheet("background-color : lightgrey")

        self.buttonG = QPushButton("Oral Sex", self)
        self.buttonG.setGeometry(200, 850, 200, 60)
        self.buttonG.setCheckable(True)
        self.buttonG.clicked.connect(self.click_oral)
        self.buttonG.setStyleSheet("background-color : lightgrey")

        self.buttont = QPushButton("torso Stiff", self)
        self.buttont.setGeometry(200, 950, 200, 60)
        self.buttont.setCheckable(True)
        self.buttont.clicked.connect(self.click_tstiff)
        self.buttont.setStyleSheet("background-color : lightgrey")

        self.ButtonGroup = QButtonGroup(self)
        self.ButtonGroup.addButton(self.button)
        self.ButtonGroup.addButton(self.button2)
        self.ButtonGroup.addButton(self.button3)
        self.ButtonGroup.addButton(self.button4)
        self.ButtonGroup.addButton(self.button5)
        self.ButtonGroup.addButton(self.button6)
        self.ButtonGroup.addButton(self.buttonE)
        self.ButtonGroup.addButton(self.buttonF)
        self.ButtonGroup.addButton(self.buttonG)
        self.ButtonGroup.addButton(self.buttont)


        # show all the widgets
        self.update()
        self.show()
    def click1(self):
        self.W['motion state'] = 'R'
        self.W['sound state'] = 'idle'
        self.statusBar().showMessage('Relax Mode Activated')
    def click2(self):
        self.W['motion state'] = 'A'
        self.W['sound state'] = 'idle'
        self.statusBar().showMessage('Laying Down  Activated')
    def click3(self):
        self.W['motion state'] = 'F'
        self.W['sound state'] = 'idle'
        self.statusBar().showMessage('Sittting Pose Activated')
    def click4(self):
        self.W['motion state'] = 'R'
        self.W['sound state'] = 'sex'
        self.statusBar().showMessage('Sex - Relaxed Activated')
    def click5(self):
        self.W['motion state'] = 'M'
        self.W['sound state'] = 'sex'
        self.statusBar().showMessage('Sex - Missionary Activated')
    def click6(self):
        self.W['motion state'] = 'D'
        self.W['sound state'] = 'sex'
        self.statusBar().showMessage('Sex - Doggy Activated')
    def clickE(self):
        self.W['power on'] = 0
        self.statusBar().showMessage('Exit Program')
        self.close()
    def click_curl(self):
        self.W['motion state'] = 'C'
        self.W['sound state'] = 'idle'
        self.statusBar().showMessage('Curl  Activated')
    def click_oral(self):
        if self.W['head motion'] == 'oral sex' :
            self.W['head motion'] = 'random'
            self.W['sound state'] = 'idle'
            self.statusBar().showMessage('Oral sex deactivated')
        else:
            self.W['head motion'] = 'oral sex'
            self.W['sound state'] = 'sex'
            self.statusBar().showMessage('Oral sex activated')
    def click_tstiff(self):
        if self.W['stiff spine'] == '1' :
            self.W['stiff spine'] = '0'
            self.statusBar().showMessage(' stiff torso deactivated')
        else:
            self.W['stiff spine'] = '1'
            self.statusBar().showMessage(' stiff torso activated')


def create_window(W):
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window(W)
    # start the app
    sys.exit(App.exec())
    window()
'''

if __name__ == '__main__':
    # create pyqt5 app
    #App = QApplication(sys.argv)
    # create the instance of our Window
    #window = Window()
    # start the app
    #sys.exit(App.exec())
    #window()
    x = 1
