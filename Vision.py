
import cv2
import time
import numpy as np
#import face_recognition as FR



##--------------------------Main Function-----------------------------------

def create_vision( world ):

    init_camera(world['camera port'])
    init_yoloface()
    print('vision on')
    while world['power on']:
        sleeptime = 1
        
        if world['vision state'] == 'face':
            left, right = snapshot()
            
            centersl = Yoloface(left)
            centersr = Yoloface(right)
            world['l faces'] = centersl
            world['r faces'] = centersr
            #print(centersl)

            sleeptime = 0.05 
            
            
            
        time.sleep(sleeptime)
    release_camera()


##---------------------------------------------------------------------------------



### this is the main function that the core calls
def play_mode(state, var1, var2, vision_mode):
    img = snapshot()

    result = detect_face_cascade(img)
    return result



def init_camera( cam_num ):
    global cap
    
    if cam_num == -1 :
        a, ports, b = list_cameras()
        if ports != []:
            cam_num = ports[0]
    
    cap = cv2.VideoCapture( cam_num )
    # resolutions for dual camera are 2560 x 720, 1280x720, 1280x480, 640x480, 640x240
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #init_FR()

def list_cameras():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            #print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Camera Port %s " %(dev_port))
                working_ports.append(dev_port)
            else:
                #print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

## takes a picture, returns picture data
## often camera has a startup time and first few pics are bad
# returns left and right images (from perspective of robot)
def snapshot():
    ret, frame = cap.read()
    if ret==True:
        #print(" sucess in image capture ")
        #frame = cv2.transpose( frame )
        frame = cv2.flip( frame, flipCode=0 )  # rotate on x axis
        width = frame.shape[1]
        width_cut = width //2
        right = frame[:, :width_cut]
        left = frame[:, width_cut:]
        
        return left ,right
    else:
        print(" failed in image capture ")



def release_camera():
    cap.release()

def save( name , img ):
    boo = cv2.imwrite( name , img )
    return boo

def init_cascade():
    global faceCascade
    faceCascade = cv2.CascadeClassifier("vision/faces.xml")

# detects the face using cascade detector
# returns a list of faces with their x and y coordinates. and also FaceID of zero (unknown)
def detect_face_cascade( img ):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale( gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
    #print( "Found {0} faces!".format(len(faces)))

    face_list = []
    for x,y,w,h in faces:
        # draws rectangle around faces
        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        item = []
        item.append(x+w/2)
        item.append(y+h/2)
        item.append(0)
        face_list.append(item)
    return face_list

def init_FR():
    pic_master  = FR.load_image_file("vision/master.png")
    global master_encoding
    master_encoding = FR.face_encodings(pic_master)

def detect_face_FR( img ):
    global face_locations
    face_locations = FR.face_locations(img)
    #print(face_locations)
    FL = []
    for top, right, bottom, left in face_locations:
        x = (right + left) /2
        y = (top + bottom) /2
        FL.append([x,y])
    return FL

# returns a list of booleans for each face, True means it matches the pic of master
def recognize_face_FR(img):
    face_encodings = FR.face_encodings(img, face_locations)
    f_list = []
    for f in face_encodings:
        results = FR.compare_faces(master_encoding, f)

        f_list.append(results[0])
    return f_list

# this function initialize camera and takes snapshopts. saves as well
def take_snapshots():
    init_camera(0)
    init_cascade()
    while 1:
        data = snapshot()
        save('test.jpg', data)
        faces = detect_face_cascade(data)
        print(faces)

########### Khadas yolo face #############
from ksnn.api import KSNN
from ksnn.types import *
from vision import YoloFace as YF

def init_yoloface():
    global yoloface
    yoloface = KSNN('VIM3')
    print(' |---+ KSNN Version: {} +---| '.format(yoloface.get_nn_version()))

    print('Start init neural network ...')
    yoloface.nn_init(library='./vision/libs/libnn_yolov3-face.so', model='./vision/models/VIM3/yolov3-face.nb', level=0)
    print('Done.')

## This function take as input an opencv image and runs face detection on it
## the output is a list of faces with data [score , xmiddle, ymiddle] 
## x and y values are from 0-1 and depend on image size
def Yoloface( img ):
    cv_img = list()
    cv_img.append(img)
    
    start = time.time()
    data = yoloface.nn_inference(cv_img, platform='DARKNET', reorder='2 1 0', output_tensor=3, output_format=output_format.OUT_FORMAT_FLOAT32)
    end = time.time()
    #print('inference time : ', end - start)

    boxes, scores = YF.yoloface_post_process( data)
    
    # draws box around original image
    #if boxes is not None:
    #    img = YF.draw(img, boxes, scores)
    
    centers = []
    if boxes is not None:
        for box, score in zip(boxes, scores):
            x, y, w, h = box
            xmid = x+w/2
            ymid = y+h/2
            #print('head at x: ' + str(xmid) + ' y: ' + str(ymid) )
            center = [xmid, ymid, score]
            centers.append( center  )   

    
    return centers

########### Khadas yolo3 (different objects detection) #############
from ksnn.api import KSNN
from ksnn.types import *
from vision import Yolov3 as Y3

def init_yolo3():
    global yolo3
    yolo3 = KSNN('VIM3')
    print(' |---+ KSNN Version: {} +---| '.format(yolo3.get_nn_version()))

    print('Start init neural network ...')
    yolo3.nn_init(library='./vision/libs/libnn_yolov3.so', model='./vision/models/VIM3/yolov3.nb', level=0)
    print('Done.')

def Yolo3( img ):
    cv_img = list()
    cv_img.append(img)
    
    start = time.time()
    data = yolo3.nn_inference(cv_img, platform='DARKNET', reorder='2 1 0', output_tensor=3, output_format=output_format.OUT_FORMAT_FLOAT32)
    end = time.time()
    print('inference time : ', end - start)
        
  
    boxes, classes, scores = Y3.yolov3_post_process(input_data)

    if boxes is not None:
        img = Y3.draw(img, boxes, scores, classes)

    return img


########### test code

if __name__ == '__main__':
    init_camera(0)
    init_yoloface()
    
    while 1:
       
        left, right = snapshot()
    
        centersl = Yoloface(left)
        centersr = Yoloface(right)
        
        print(centersl)
        print(centersr)

        
        
        
        time.sleep(0.1)
