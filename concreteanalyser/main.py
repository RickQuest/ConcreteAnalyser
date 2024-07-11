from printer_stage import PrinterStage
from base_microscope import BaseMicroscope
from analyser import Analyser
from threading import Thread
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
import os 
import time

def main():
    print(cv2.__version__)

    # analyser=Analyser([25,108,76])
    # thread1 = Thread(target = analyser.stream, args = ())
    # thread1.start()
    # analyser.scan("scan3",1,4,15)
    # thread1.join()

    scanpath = os.getcwd()+"\\scans\\scan3\\traverse0"
    # scanpath = os.path.split(os.getcwd())[0]+"\\scans\\scan1\\traverse1"
    Analyser.stitch2(scanpath,show=False, export=True) 
    
    # analyser.stage.home(True,True,True)
    # analyser.calPosition=[0,135.5,76.8]
    # analyser.startPosition = [15,117.5,76]
    # analyser.calibration("scan1")
    # analyser.autofocus()    
    # stitch = np.load('tests\\test1\\scan 0\\stitch.npy',allow_pickle=True)
    # cropped_stitch = Analyser.crop_stitch(stitch,'tests\\test1\\scan 0')
    # Analyser.show_stitch(cropped_stitch)
    # Analyser.show_stitch('tests\\test2(3)\\scan0\\stitch.npy')


if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    