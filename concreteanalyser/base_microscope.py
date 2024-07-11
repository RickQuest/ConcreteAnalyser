import cv2  
import time 
from threading import Thread 
from serial.tools import list_ports

class BaseMicroscope :
    def __init__(self, stream_id=0):
        self.stream_id = stream_id # default is 0 for main camera 
        self.windowname = 'microscope stream'
        # opening video capture stream 
        self.vcap      = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)  # set new dimensionns to cam object (not cap)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
        fps_input_stream = int(self.vcap.get(5)) # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream)) 

        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False 
        self.stopped = True
        # thread instantiation  
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads run in background 

        
    # method to start thread 
    def start(self):
        self.stopped = False
        self.t.start()
        
    # method passed to thread to read next available frame  
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()

    # method to return latest read frame 
    def read(self):
        return self.frame

     
    def stream(self):
        while(True): 
            # cv2.imshow(self.windowname, cv2.resize(self.frame, (1920, 1080)))
            cv2.imshow(self.windowname, self.frame)
            if self.stopped is True :
                break    

        cv2.destroyWindow(self.windowname)
    # method to stop reading frames
    def stop(self):
        self.stopped = True

