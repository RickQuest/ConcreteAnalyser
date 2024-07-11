import os
import sys
import cv2
import math
# from cv2 import Stitcher
from stitching.stitcher import Stitcher
from matplotlib import pyplot as plt
from scipy.io import savemat
import time 
import numpy as np
from skimage import morphology
import imutils
from base_microscope import BaseMicroscope #. deleted for test
from printer_stage import PrinterStage #. deleted for test
import glob
from PIL import Image

class Analyser():

    def __init__(self,startPosition):
        self.__calPosition = [0,0,0]
        self.startPosition = startPosition
        self.pixelsize=0
        self.iscamalign = False
        self.microscope=BaseMicroscope(0)
        self.microscope.start()
        self.stage=PrinterStage()
        self.save_directory=os.getcwd()+"\\scans\\"
        self.scanfolder = ""
        if not os.path.exists(self.save_directory):
            os.mkdir(self.save_directory)
        self.image_format="jpeg"
        self.x_inc = 1.5
        self.y_inc= 20
        self.windowname='Microscope viewer'
        # cv2.namedWindow(self.windowname, cv2.WINDOW_NORMAL)


    @property
    def calPosition(self):
         return self.__calPosition
    @calPosition.setter
    def calPosition(self, a):
        #  if(a < 18):
        #     raise ValueError("Sorry you age is below eligibility criteria")
        #  print("setter method called")
         self.__calPosition = a

    def __del__(self):
      self.microscope.stop()

    def create_scandir(self,scanname):
        scanfolder = os.path.join(self.save_directory,scanname)
        print(scanfolder)
        if not os.path.exists(scanfolder):
            os.mkdir(scanfolder)
        else:
            count=1

            while(True):
                if not os.path.exists(scanfolder+"({})".format(count)):
                    scanfolder+="({})".format(count)
                    os.mkdir(scanfolder)
                    break
                else:
                    count+=1
            
            print("Directory " , scanname ,  " created at ",scanfolder)
        self.scanfolder = scanfolder

    def stream(self):
        num_frames_processed = 0 
        start = time.time()
        while True :
            if self.microscope.stopped is True :
                break
            else :
                frame = self.microscope.read()
            # adding a delay for simulating video processing time 
            time.sleep(0.03) 
            num_frames_processed += 1
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            # frame = cv2.putText(frame, str(fm), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) 
            cv2.imshow(self.windowname , frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):    
                break

        end = time.time()
        elapsed = end-start
        fps = num_frames_processed/elapsed 
        print("FPS: {} , Elapsed Time: {} ".format(fps, elapsed))
        cv2.destroyWindow(self.windowname)

    def scan(self,scanname,step_distance,traverse_number,focus_steps):
        step_number = math.floor((100-5)/step_distance)
        self.stage.start()
        self.create_scandir(scanname)
        self.stage.moveZ(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[2])
        self.stage.moveX(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[0])
        self.stage.moveY(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[1]+10)
        # self.printer.moveZ(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, 56)
        time.sleep(20)
        self.autofocus(2)
        yDirection = 1
        step_counter = 0
        for y in range(traverse_number):
            traversefolder = os.path.join(self.scanfolder,"traverse{}".format(y))
            os.mkdir(traversefolder)
            time.sleep(1)
            for x in range(step_number):
                imgpath = os.path.join(traversefolder,"x{:02d}y{:02d}.".format(x,y))+self.image_format
                cv2.imwrite(imgpath, self.microscope.read())
                self.stage.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, step_distance*yDirection)
                step_counter +=1
                if step_counter ==focus_steps:
                    self.autofocus()
                    step_counter=0
            # self.stitch2(traversefolder,True,True)
            self.stage.moveX(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 200/traverse_number)
            step_counter=0
            time.sleep(5)
            self.autofocus()

            yDirection = yDirection*-1

        self.stage.stop()

    def scan2(self,scanname,step_distance,traverse_number,focus_steps):
        step_number = math.floor(100/step_distance)
        self.stage.start()
        scanfolder = self.create_scandir(scanname)
        self.stage.moveZ(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[2])
        self.stage.moveX(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[0])
        self.stage.moveY(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.startPosition[1]+10)
        time.sleep(30)
        self.autofocus(1)
        self.stage.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, -10) 
        time.sleep(10)
        yDirection = 1
        step_counter = 0
        for x in range(traverse_number):
            trasversefolder = os.path.join(scanfolder,"traverse{}".format(x))
            os.mkdir(trasversefolder)
            time.sleep(1)
            for y in range(step_number):
                if y==24:
                    self.stage.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 4*yDirection)
                elif y==0:
                    self.stage.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, step_distance*yDirection)
                    # time.sleep(1)   
                    # self.printer.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 1*yDirection)
                    # time.sleep(1)   
                    # self.printer.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, -1*yDirection)
                    # time.sleep(5)   
                else:
                    self.stage.moveY(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, step_distance*yDirection)
                time.sleep(1)
                scanpath = os.path.join(trasversefolder,"x{:02d}y{:02d}.".format(x,y))+self.image_format
                cv2.imwrite(scanpath, self.microscope.read())
                step_counter +=1
                if step_counter ==focus_steps:
                    self.autofocus()
                    step_counter=0
            self.stage.moveX(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 10)
            yDirection = yDirection*-1
        self.stage.stop()

    def autofocus(self,factor=1):
        direction = 1
        frame = self.microscope.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lastfocus = cv2.Laplacian(gray, cv2.CV_64F).var()

        self.stage.moveZ(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 0.1*factor)
        time.sleep(1*factor)
        frame = self.microscope.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        upfocus = cv2.Laplacian(gray, cv2.CV_64F).var()

        self.stage.moveZ(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, -0.2*factor)
        time.sleep(1*factor)
        frame = self.microscope.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        downfocus = cv2.Laplacian(gray, cv2.CV_64F).var()

        #Return to initial position
        self.stage.moveZ(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 0.1*factor)
        time.sleep(1*factor)

        if lastfocus>=upfocus and lastfocus>=downfocus :
            print('Last focus better')
            return
        elif downfocus<=upfocus :
            direction =1
            print('Up focus better')
        elif upfocus<=downfocus :
            direction =-1
            print('Down focus better')
        else:
            raise Exception("Sorry, unhandled exception occur during autofocus")


        while True:
            self.stage.moveZ(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 0.1*direction)
            time.sleep(1)
            frame = self.microscope.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            focus = cv2.Laplacian(gray, cv2.CV_64F).var()
            if lastfocus <= focus :
                lastfocus = focus
            else :
                self.stage.moveZ(PrinterStage.Positioning.relative, PrinterStage.MoveMode.linear, 0.1*-direction)
                break
    
    def calibration(self,scanname):
        #Move to calibration position
        self.stage.moveZ(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.__calPosition[2])
        # self.stage.moveX(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.__calPosition[0])
        self.stage.moveY(PrinterStage.Positioning.absolute, PrinterStage.MoveMode.linear, self.__calPosition[1])
        time.sleep(30)
        self.autofocus(2)
        time.sleep(1)
        #Get frame of calibration staple and convert to binary
        img = self.microscope.read()
        scanfolder = self.create_scandir(scanname)
        imgFilename=os.path.join(scanfolder,"calibrationRGB."+self.image_format)
        cv2.imwrite(imgFilename,img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        M = img.shape[0]
        N = img.shape[1]
        BW = img<90
        # ret,BW = cv2.threshold(img,90,0,cv2.THRESH_BINARY)
        plt.imshow(BW*255)
        plt.show()
        #Filter the binary and save result for proof of calibration
        BW = morphology.remove_small_objects(BW, min_size=200, connectivity=4)
        BW = morphology.binary_closing(BW, morphology.disk(20), out=None)
        plt.imshow(BW*255)
        plt.show()
        (rows, columns) = np.where( BW )
        assert np.count_nonzero(BW)>200, "No calibration shape was detected"
        BWFilename=os.path.join(scanfolder,"calibrationBW."+self.image_format)
        cv2.imwrite(BWFilename,BW*255)
        #Get required information
        
        maxC = max(columns)
        minC=min(columns)
        maxR=max(rows)
        minR=min(rows)
        minY = np.empty(N, dtype=int) 
        maxY = np.empty(N, dtype=int) 
        for i in range(N):
            # [rows,columns] = np.argwhere(BW[:,i] == 1)#np.where(BW[:,i])
            rows = np.where(BW[:,i])

            minY[i]=min(rows)
            maxY[i]=max(rows)
        #Check camera alignement
        lminmean=np.mean(minY[minC:100])
        rminmean=np.mean(minY[maxC-100:maxC])
        align = abs(lminmean-rminmean)
        self.iscamalign = True if align<25 else False   
        #Find pixel size
        minY_mean=np.mean(minY)
        maxY_mean=np.mean(maxY)
        width=round(maxY_mean-minY_mean)
        self.pixelsize=0.076/width
        

    @staticmethod
    def images2numpy(scanfolder):
        filelist = glob.glob(scanfolder + '**/*.jpeg')
        # x = np.array([np.array(Image.open(fname).convert('L')) for fname in filelist])
        x = np.array([np.array(Image.open(fname)) for fname in filelist])
        x.dump(os.path.join(scanfolder,'images.npy'))
    
    @staticmethod
    def stitch2(scanfolder,show = False, export=False):
        #https://github.com/lukasalexanderweber/stitching_tutorial/blob/master/docs/Stitching%20Tutorial.md
        filelist = glob.glob(scanfolder + '**/*.jpeg')
        filelist = [ x for x in filelist if "stitch" not in x ]
        settings = {"matcher_type": "affine",   
                    "estimator": "affine", 
                    "adjuster": "affine",        
                    "wave_correct_kind": "no",  
                    "warper_type": "affine", 
                    "try_use_gpu": False,     
                    # The whole plan should be considered
                    "crop": True,
                    # The matches confidences aren't that good
                    "confidence_threshold": 0.5,
                    # "medium_megapix": 6,  
                    # "low_megapix": 1,
                    # "final_megapix":0
                    }  
        tic = time.perf_counter()
        stitcher = Stitcher(**settings)
        panorama = stitcher.stitch(filelist)
        toc = time.perf_counter()
        print(f"Stitch time : {toc - tic:0.4f} seconds")
        if show :
            Analyser.plot_image(panorama, (20,20)) 
        if export :
            cv2.imwrite(scanfolder+"\\stitch.tiff", panorama)
            # Analyser.save_stitch(panorama,scanfolder,"stitch")
        # return panorama

    @staticmethod
    def save_stitch(stitch,scanfolder,filename):
        image_array = np.array(stitch)
        numpy_filename = os.path.join(scanfolder,filename+'.npy')
        matlab_filename = os.path.splitext(numpy_filename)[0]+'.mat'
        image_array.dump(numpy_filename)
        savemat(matlab_filename, {'X': image_array})

    @staticmethod
    def show_stitch(stitch):
        if isinstance(stitch, str):
            stitch = np.load(stitch,allow_pickle=True)
        Analyser.plot_image(stitch)

    @staticmethod
    def plot_image(img, figsize_in_inches=(5,5)):
        fig, ax = plt.subplots(figsize=figsize_in_inches)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()

    @staticmethod
    def crop_stitch(stitched,scanfolder=None):
        if isinstance(stitched, str):
            stitched = np.load(stitched,allow_pickle=True)
        
        stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        minRect = mask.copy()
        sub = mask.copy()
        while cv2.countNonZero(sub) > 0:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        stitched = stitched[y:y + h, x:x + w]
        if scanfolder is not None:
            Analyser.save_stitch(stitched,scanfolder,"cropped_stitch")
            # stitched.dump(save)
        return stitched

