import serial
import time
from datetime import datetime
from enum import Enum
from base_stage import BaseStage #. deleted for test

class PrinterStage(BaseStage):

  class Positioning(Enum):
    relative = "G91"
    absolute = "G90"

  class Units(Enum):
    millimeters = "G21"
    inches = "G20"

  class MoveMode(Enum):
    rapid = "G0"
    linear = "G1"

#region abstract method
  def __init__(self):
    super().__init__()
    self.port='COM3'
    self.stagezone= [210,210,205]
    self.baudrate = 250000
    # self.parity=super().parity
    # self.bits=super().bits
    self.connection = serial.Serial(self.port, self.baudrate)
    self.xyzcoord=[0,0,0]
    time.sleep(2)
    print("3D printer initialization complete")

  def __del__(self):
    self.connection.close()

  def send_command(self,ser, command):
      start_time = datetime.now()
      ser.write(str.encode(command)) 
      time.sleep(1)

      while True:
        line = ser.readline()
        # print("RECEIVE:")
        print(line)

        if line == b'ok\n':
          break

  def home(self,x=True,y=True,z=True):
    command = "G28"
    command+=" X" if x else ""
    command+=" Y" if y else ""
    command+=" Z" if z else ""
    command+="\r\n"
    self.send_command(self.connection, command)

  def stop(self):
    self.fan_off()
    self.extruder_off()
    self.bed_off()
    self.motor_off()
    self.moveZ(self.Positioning.absolute, self.MoveMode.linear, 80)
    self.home(True,True,False)
    self.home(False,False,True)

  def start(self):
    self.set_units(self.Units.millimeters)
    self.set_positioning(self.Positioning.absolute)
    self.home(True,True,False)
    self.home(False,False,True)

  def moveZ(self,positioning :Positioning, mode: MoveMode, z):
    if z>self.stagezone[2]:
      print("Position parameter is outisde the range")
      return
    self.set_positioning(positioning)
    command = mode.value+" Z{}\r\n".format(z)
    self.send_command(self.connection, command)

  def moveY(self,positioning :Positioning, mode: MoveMode, y):
    if y>self.stagezone[1]:
      print("Position parameter is outisde the range")
      return
    self.set_positioning(positioning)
    command = mode.value+" Y{}\r\n".format(y)
    self.send_command(self.connection, command)

  def moveX(self,positioning :Positioning, mode: MoveMode, x):
    if x>self.stagezone[0]:
      print("Position parameter is outisde the range")
      return
    self.set_positioning(positioning)
    command = mode.value+" X{}\r\n".format(x)
    self.send_command(self.connection, command)

  def move(self,mode: MoveMode ,x,y,z):
    if x>self.stagezone[0] or y>self.stagezone[1] or z>self.stagezone[2]:
      print("Position parameter is outisde the range")
      return
    # command = "G90 X{} Y{} Z{} F{}\r\n".format(x,y,z,v)
    command = mode.value+" X{} Y{} Z{}\r\n".format(x,y,z)
    self.send_command(self.connection, command)
#endregion

#region this class method
  def fan_on(self,speed):
    if speed<0 or speed>255:
      print("speed parameter is outside the range (0<speed<255)")
      return
    command="M106 S{}\r\n".format(speed)
    self.send_command(self.connection, command)

  def fan_off(self):
    command="M107\r\n"
    self.send_command(self.connection, command)

  def bed_off(self):
    command="M140 S0\r\n"
    self.send_command(self.connection, command)

  def extruder_off(self):
    command="M104 S0\r\n"
    self.send_command(self.connection, command)  

  def motor_off(self):
    command="M84\r\n"
    self.send_command(self.connection, command)

  def set_positioning(self,mode: Positioning):
    command=mode.value+"\r\n"
    self.send_command(self.connection, command)

  def set_units(self,mode: Units):
    command=mode.value+"\r\n"
    self.send_command(self.connection, command)
#endregion





 