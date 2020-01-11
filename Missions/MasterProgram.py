#!/usr/bin/env python3

# FLL 42, Pythonian Rabbotics's master program. Copyright (c) 2019 FLL team 42

#---------------------------------------------------Imports and variable definitions-----------------------------------------------------------------
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import time
import sys
btn = Button() # variable so we can get buttons pressed on EV3
color = ColorSensor(INPUT_4) # color sensor for checking attachment color
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)  # Creates a variable so we can control the drivetrain
motorA = MediumMotor(OUTPUT_A) # left medium motor
motorD = MediumMotor(OUTPUT_D) # right medium motor
gyro = GyroSensor(INPUT_1) # gyro variable
Sound_ = Sound() # beepity beep
Display_ = Display() # for displaying text
Sound_.play_tone(frequency=400, duration=0.5, volume=50) #plays a note so we know when the code starts
#---------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------Distance conversion--------------------------------------------------------------------------------
# Distance Conversion
wheelDiameter_mm = 56 # Look at the first number on the NUMBERxNUMBER on wheel
wheelCircumference_cm = (wheelDiameter_mm/10) * 3.14159265358979323846284338 # Convert to cm and multiply by pi for circumference
wheelCircumference_in = (wheelDiameter_mm/25.4) * 3.14159265358979323846284338 # Convert to in and multiply by pi for circumference
# inches to rotations:
# example: drive.on_for_rotations(SpeedPercent(100), SpeedPrecent(100), inToRotations(5))
# to go 5 inches
def inToRotations(inches):
    return inches/wheelCircumference_in
# centimeters to rotations:
# example: drive.on_for_rotations(SpeedPercent(100), SpeedPrecent(100), cmToRotations(5))
# to go 5 centimeters
def cmToRotations(cm):
    return cm/wheelCircumference_cm
# inches to millimeters:
def inToMillimeters(inches):
    return inches * 25.4
# centimeters to millimeters:
def cmToMillimeters(cm): #hhm it works... questionable -- no syntax errors!
    return cm * 10 # Yay, no syntax errors!
def drive_cm(power, cm):
    rt = cmToRotations(cm)
    tank_drive.on_for_rotations(SpeedPercent(power), SpeedPercent(power), int(rt) )
def drive_cm_new(power, cm):
    rt = cmToRotations(cm)
    tank_drive.on_for_rotations(SpeedPercent(power), SpeedPercent(power), rt)
#---------------------------------------------------------------------------------------------------------------------------------------------

def gyroTurn(deg, speedL, speedR):
    startAng = gyro.angle # get current gyro angle
    if deg >= 0: # if we're turning right,
        while (gyro.angle-startAng) <= deg: # while the current turned angle is less than the angle we want to turn to,
            tank_drive.on(SpeedPercent(speedL), SpeedPercent(speedR)) # turn
    if deg < 0: # if we're turning left, 
        while (gyro.angle-startAng) >= deg: # while the current turned angle is greater than the angle we want to turn to,
            tank_drive.on(SpeedPercent(speedL), SpeedPercent(speedR)) # turn
    tank_drive.off() # stop turning at the end
#------------------------------------GyroStraight------------------------------------------------------------------------------------------------------#
def gyroStraight(rotations):
    startAng = gyro.angle
    if deg >= 0:
        while (gyro.angle-startAng) <= deg:
            tank_drive.on_for_rotations(SpeedPercent(30), SpeedPercent(40), rotations)
    if deg < 0:
        while (gyro.angle-startAng) <= deg:
            tank_drive.on_for_rotations(SpeedPercent(40), SpeedPercent(30), rotations)
    tank_drive.off()



#-----------------------------------yellow = swing and safety by Alan and Kunal---------------------------------------------------------------
def swing_and_safety():

    motorD.stop_action = motorD.STOP_ACTION_HOLD
    motorD.stop() # stall right motor

    tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 6.67) #ROBOT MOVES FORWARD FROM BASE
    tank_drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.9000003141592653589) # ROBOT MOVES INTO SWING
    tank_drive.on_for_rotations(SpeedPercent(-30), SpeedPercent(-30), 0.4) #ROBOT MOVES AWAY FROM SWING

    motorD.stop_action = motorD.STOP_ACTION_COAST
    motorD.stop() # unstall right motor

    tank_drive.on_for_rotations(SpeedPercent(-30), SpeedPercent(0), 1.5) #ROBOT TURNS TO SQUARE ON WALL
    motorA.on_for_degrees(SpeedPercent(15), 150) #LEFT ARM TURNS FOR ELEVATOR
    tank_drive.on_for_rotations(SpeedPercent(-15), SpeedPercent(-15), 0.666666666666666666) # ROBOT MOVES BACK INTO WALL
    tank_drive.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 1.8) #ROBOT MOVES FORWARD TO ELEVATOR
    tank_drive.on_for_rotations(SpeedPercent(30), SpeedPercent(0), 1) #ROBOT TURNS CLOCKWISE TO FACE ELEVATOR
    tank_drive.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 1.25) #ROBOT MOVES FORWARD AND HITS ELEVATOR
    motorA.on_for_degrees(SpeedPercent(15), 200)#MEDIUM MOTOR TURNS AWAY SO IT DOESN'T UNDO ELEVATOR
    tank_drive.on_for_rotations(SpeedPercent(0), SpeedPercent(-30), 0.80000314159265358979323816264338)#ROBOT TURNS TO SAFETY FACTOR
    tank_drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 1.1000000042424242424242424242424242)#ROBOT MOVES INTO SAFETY FACTOR
    tank_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.3)#ROBOT TURNS TO KNOCK DOWN BEAMS
    tank_drive.on_for_rotations(SpeedPercent(-15), SpeedPercent(-15), 0.25) # ROBOT MOVES BACK TO NOT KNOCK DOWN THE BUILDING IN SAFETY FACTOR
    tank_drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(10), 0.5)#ROBOT TURNS TO KNOCK DOWN BEAMS
    tank_drive.on_for_rotations(SpeedPercent(-60), SpeedPercent(-60), 12) # ROBOT MOVES BACK TO BASE
    motorA.stop_action = motorA.STOP_ACTION_COAST
    motorA.stop() # unstall left motor
#------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------- Big Design and Build is green ----------------------------------------------------------

def big_design_and_build():
    drive_cm(50, 65) # go forward to drop off stuff
    tank_drive.on_for_seconds(SpeedPercent(-10), SpeedPercent(-50), 2) # turn right
    drive_cm(-20, 65) # back into home sweet home

#--------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------ red = Design & Build 1 --------------------------------------------------------

def design_and_build_one():
    drive_cm_new(50,45) # forward
    gyroTurn(-26,0,50) # turn toward tan
    drive_cm_new(50,75) # wheeeeee
    drive_cm_new(50,-46) # drop tan
    motorD.on_for_degrees(25,80) # opens gate
    drive_cm_new(50, -10) # go back
    gyroTurn(35,50,0) # turn
    drive_cm_new(70,-110) # back to home sweet homes


#--------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------blue = crane & innovative architecture by Yash and Alan--------------------------------------------------------------------
def crane():
    drive_cm_new(50,42) # drive forward
    drive_cm_new(50,-23) # drive back (drops off wabbit)
    gyroTurn(-39, 0, 50) # turn toward crane
    drive_cm_new(35,30) #drops crane
    drive_cm_new(50,-51) # drive back so we don't run into big D&B
    gyroTurn(90, 50, 0) # turn right
    drive_cm_new(70,-60) # drive back into home sweet home
#--------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------black = Elevated Places/Bridge - Ben & Joshua-------------------------------------------------------------
def elevated_places():
    drive_cm_new(65,-127.5) #drive out(backwards so that it can fit up the bridge better) and stop just before the swing | 65% speed -- fast whoosh
    gyroTurn(-90,-15,15)#turns so that the front of the robot faces the wall
    drive_cm_new(60,30) #drives forwards and square on the front of the robot (back of the robot facing bridge)
    drive_cm_new(30,-20) #drives backwards to get in a better postion to drive up the bridge
    gyroTurn(-20,-15,15) # final positioning turn 
    drive_cm_new(30,-119) # drives backwards up bridge
    tank_drive.off() # stalls drivetrain
    while True:
        if (btn.enter):
            tank_drive.off(brake=False) # Unstalls motors
            break
        time.sleep(0.25)
#--------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------- creating the function ColorChecking ---------------------------------------------------------------
def ColorChecking():
    if color.color == color.COLOR_YELLOW: #if yellow
        swing_and_safety()
    elif color.color == color.COLOR_GREEN: #if green
        big_design_and_build()
    elif color.color == color.COLOR_RED: #if red
        design_and_build_one()
    elif color.color == color.COLOR_BLUE: #if blue
        crane()
    elif color.color == color.COLOR_BLACK: # if black
        elevated_places()
#--------------------------------------------------------------------------------------------------------------------------------------------

#This is where the movement happens. the function "ColorChecking" is a function to decide what to do based on color.

#--------------- failsafe -------------
def failsafe():
    sys.exit()
#--------------------------------------

#now whenever we touch enter (or the middle button) then it will call ColorChecking().
Sound_.play_tone(frequency=400, duration=0.5, volume=50)
start = time.time()
btn.on_backspace = failsafe

while True: #this code essentially color checks forever
    if (btn.down):
        break
    pass
    btn.wait_for_released('enter')
    ColorChecking()

# Beepity beep!
Sound_.play_tone(frequency=400, duration=0.5, volume=50)