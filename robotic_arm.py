#!/usr/bin/python
 
import spidev
import os
import time

import RPi.GPIO as GPIO
import time
 
# Define Axis Channels (channel 3 to 7 can be assigned for more buttons / joysticks)
swt_channel = 0
vrx_channel = 1
vry_channel = 2
 
#Time delay, which tells how many seconds the value is read out
delay = 0.2
 
# Spi oeffnen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

arm_section = 1

lift_pin = 37 
gripper_pin = 35
base_pin = 33
top_pin = 31
middle_pin = 29 
camera_pin = 13 

CLOSE = 5.0
OPEN = 10.0

FREQ = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gripper_pin, GPIO.OUT)
GPIO.setup(lift_pin, GPIO.OUT)
GPIO.setup(base_pin, GPIO.OUT)
GPIO.setup(top_pin, GPIO.OUT)
GPIO.setup(middle_pin, GPIO.OUT)
GPIO.setup(camera_pin, GPIO.OUT)

pwm_lift = GPIO.PWM(lift_pin, FREQ)
pwm_gripper = GPIO.PWM(gripper_pin, FREQ)
pwm_base = GPIO.PWM(base_pin, FREQ)
pwm_top = GPIO.PWM(top_pin, FREQ)
pwm_middle = GPIO.PWM(middle_pin, FREQ)
pwm_camera = GPIO.PWM(camera_pin, FREQ)

pwm_lift.start(CLOSE)
pwm_gripper.start(CLOSE)
pwm_base.start(CLOSE)
pwm_top.start(CLOSE)
pwm_middle.start(CLOSE)
pwm_camera.start(CLOSE)

# Function for reading the MCP3008 channel between 0 and 7
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data
 
 
# endless loop
while True:
  arm_section = input( "Enter Arm Section ( 1 - Gripper, 2 - Arm, 3 - Camera):" )

  if( arm_section <> 1 and arm_section <> 2 and arm_section <> 3):
    print( "Wrong Arm Section entered" )

  else:
    while True:

      # Determine position
      vrx_pos = readChannel(vrx_channel)
      vry_pos = readChannel(vry_channel)
 
      # SW determine
      swt_val = readChannel(swt_channel)
 
      # output
#  print("VRx : {}  VRy : {}  SW : {}".format(vrx_pos,vry_pos,swt_val))

      if( arm_section == 1 ):
        print( "---> Moving Gripper Arm" )

        if( vrx_pos <= 5 ):
          print("UP - BOW THE GRIPPER")

          pwm_lift.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break

        elif( vrx_pos == 1023 ):
          print("BACK - LIFT THE GRIPPER")

          pwm_lift.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break

        if( vry_pos == 1023 ):
          print("LEFT - OPEN THE GRIPPER")

          pwm_gripper.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break 

        elif( vry_pos <= 5 ):
          print("RIGHT - CLOSE THE GRIPPER")

          pwm_gripper.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break 
 
        if( swt_val <= 5 ):
          print("PRESSED")
          time.sleep(delay)
          break 

      elif( arm_section == 2 ):
        print( "---> Moving Middle Arm" )

        if( vrx_pos <= 5 ):
          print("UP - BOW THE Middle Arm")

          pwm_middle.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break

        elif( vrx_pos == 1023 ):
          print("BACK - LIFT THE Middle Arm")

          pwm_middle.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break

        if( vry_pos <= 5 ):
          print("LEFT - TURN COUNTERCLOCKWISE")

          pwm_base.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break

        elif( vry_pos == 1023 ):
          print("RIGHT - TURN CLOCKWISE")

          pwm_base.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break

        if( swt_val <= 5 ):
          print("PRESSED")
          time.sleep(delay)
          break
      elif( arm_section == 3 ):
        print( "---> Moving Camera Arm" )

        if( vry_pos <= 5 ):
          print("UP - TURM THE Camera Arm CLOCKWISE")

          pwm_camera.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break

        elif( vry_pos == 1023 ):
          print("BACK - TURN THE Camera Arm COUNTERCLOCKWISE")

          pwm_camera.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break

        if( vrx_pos <= 5 ):
          print("LEFT - Bow the Top Arm")

          pwm_top.ChangeDutyCycle(CLOSE)
          time.sleep(delay)
          break

        elif( vrx_pos == 1023 ):
          print("RIGHT - Raise the Top Arm")

          pwm_top.ChangeDutyCycle(OPEN)
          time.sleep(delay)
          break

        if( swt_val <= 5 ):
          print("PRESSED")
          time.sleep(delay)
          break

