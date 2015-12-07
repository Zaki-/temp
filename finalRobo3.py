import sys

#appends api directory path to sys path
#sys.path.append("/home/pi/Human_Robots_Interaction_Fall15")
sys.path.append("/home/pi/HROS1-Framework/Linux/project/Human_Robots_Interaction_Fall15")


import api 
import sys

from pixy import *
from ctypes import *

tempY=0
speedInc=0
timer = 0
chestX = 0
chestY=0
HeadY=0
LHX=0
RHX=0
LHY=0
RHY=0


def RoboWalk(color, trackX):   # X,Y are the center of the object that is deteced by pixy, color green move, color red stop
    global sit, walk, speedInc, timer
 #   timer = timer +1
  #  print  timer
    if (color == 'green') and (walk == False): #if the color is green and the robot is not walking let it walk

        api.Walk(True)       # set the robot in walk ready mode
	speed =10
        api.WalkMove(speed)  #the robot start to move for the given speed
        walk = True          #indicate that the robot is walikg
        sit=0                #flag that the robot is not in sit position
        #HeadMove = False     
    elif (color == 'red') and (walk == True):  #
       walk = False         #indicate that the robot not walking
       if (sit == 0):       #if the robot is not in sit position make it sit
        api.Walk(False)    #stop the walk ready mode
        api.PlayAction(15) #call the sit position - page 15
        sit=1              # flag that the robot is in sit position

#def RoboTurn(trackX):
    # Turn while walking
    if (walk == True): #if the robot is walking check the direction 
        if (trackX>10):
    	    api.WalkTurn(-5)
	    
	    print 'left'
        elif(trackX<-10):
            api.WalkTurn(5)
	    print 'right'
        else :
            api.WalkTurn(0)
#	End of RoboWalk()

def RoboInit():
    try:
                if api.Initialize():
                        print("Initalized")
                else:
                        print("Intialization failed")

    except (KeyboardInterrupt):
                api.ServoShutdown()
                sys.exit()
    except():
        api.ServoShutdown()
        sys.exit()

# End of RoboInit()
# set the Global variables
def centerX(x):
	return x-160
def centerY(y):
	return 100-y
sitFlag =True #start with the sitting position
walkFlag =False

def SetHead(x,y):
	pan=api.GetMotorValue(19)
	tilt= api.GetMotorValue(20)
	if (x>20) and (pan <600) and (pan>390):
		for i in range(1, 5):
 			api.SetMotorValue(19,pan-1)
	elif (x<-20) and (pan >380) and (pan <600):
		for i in range(1, 5):
			api.SetMotorValue(19,pan+1)
	if (y>20) and (tilt < 612) and (tilt >420):
		for i in range(1, 5):
			api.SetMotorValue(20,tilt-1)
	elif (y<-20) and (tilt > 420) and (tilt < 612):
		for i in range(1, 5):
			api.SetMotorValue(20,tilt+1)
	print 'tilt=',tilt

def WalkReady(b):
	global walkFalg,startCounter
	# counter to stop walking by itself after it counts 3000 frames
	startCounter=frame
	if (frame-startCounter) == 3000 :
		b=False
	# end of the counter
	if (b == True) and (walkFlag == False) and (sitFlag == False) :
		api.Walk(True)
		api.WalkMove(3)
		walkFlag = True
	elif (b == False) and (walkFlag == True) and (sitFlag == False):
		api.Walk(False)
		api.PlayAction(1)
		walkFlag = False



def Sit(b):#pass true to make the robot sit
	global sitFlag
	if (b == True) and (sitFlag == False):
		api.PlayAction(16)
		sitFlag = True
	elif (b == False) and (sitFlag ==True):
		api.PlayAction(1)
		sitFlag = False
		

def SoS():
	if (sitFlag == False) and (walkFlag == False):
		print 'api.PlayAction(sos)'

def UVA():
	if (sitFlag == False) and(walkFlag == False):
		print 'api.PlayAction(UVA)'
def CheckSign2(RHY, LHY, chestY, HeadY):
	print RHY



def checkSign(LHY, LHarea,RHY, RHarea,HeadY, Headarea,chestY, chestarea):
	#one of the chalenges is the rate of the edges must change with the distance
	
	HY=abs(LHY-RHY)
	avg=abs(int((LHY+RHY)/2))
	rateY=abs(HeadY-chestY)
	# stand up
	if (avg-chestY)<10:
		print 'stand'
#		WalkReady(False)
#		sit(False) #stand
	# sit down
	if (HY > 10) and (LHY>chestarea):
	#if (HY<10) and (abs(chestY-HY)-abs(int(0.3*rateY))<10) and (avg > chestY) and (avg > HeadY):
	#the distance between chestY and both hands Y(HY) almost equels half of distance between head and chest
		print 'sit'
#		WalkReady(False)
#		sit(True)
	# start walking
	if (HY<10) and (abs(HeadY-HY)-abs(int(0.3*rateY))<10) and (avg>HeadY) and (avg < chestY):
	# the distance between head and both hands Y almost equels half of  the distance between the head and chest 
		print 'walking'
#		WalkReady(True)


	# UVA
#	if (HY<10) and (RHX == LHX) and (HY > chestY):
#		UVA()
	# SoS
	if (HY<10) and (abs(HeadY-HY)-abs(int(0.3*rateY))<10) and (avg<HeadY) and (avg < chestY):
		print 'sos'
#		SoS()



sit = 0
walk = False
X=0  # 0 - 320
color = 'red'


#initialize Pixy interpreter thread
pixy_init()

#initialize the Robot movements
RoboInit()

#Blocks
class Blocks (Structure):
      _fields_ = [ ("type", c_uint),
                   ("signature", c_uint),
                   ("x", c_uint),
                   ("y", c_uint),
                   ("width", c_uint),
                   ("height", c_uint),
                   ("angle", c_uint) ]

blocks = BlockArray(100)
frame = 0
battryLim = 107
#wait for blocks
api.SetMotorValue(20,433)
try:
  while 1:
     count = pixy_get_blocks(100, blocks)
     if (int(api.BatteryVoltLevel()) <= battryLim):
      if (int(api.BatteryVoltLevel()) <= battryLim):
       if (int(api.BatteryVoltLevel()) <= battryLim):

	print 'Low Battery'
#	api.Walk(False)
#	api.PlayAction(15)
#	api.ServoShutdown()
#	sys.exit()
     else:
#       print 'Battery power', int(api.BatteryVoltLevel())
       if count > 0:
#	 
         #blocks found
	 Uframe=frame/500
         print 'frame %3d:' % (frame)
         frame = frame +1
	 #print 'RHY=%d LHY=%d chestY=%d HeadY=%d' %(RHY, LHY, chestY, HeadY)				
	 checkSign(LHY, LHarea,RHY,RHarea, HeadY, Headarea,chestY, chestarea)

         for index in range(0, count):
		# pixy reselution 320X200	     

             	if (index == 0) and (blocks[index].signature == 1):
			RHX=blocks[index].x
			RHY=blocks[index].y
			RHarea=blocks[index].height*blocks[index].width
		if (index == 1) and (blocks[index].signature == 1):
			LHX=blocks[index].x
			LHY=blocks[index].y
			LHarea=blocks[index].height*blocks[index].width

		if (index == 2) and (blocks[index].signature == 5):
			tempX=blocks[index].x
			tempY=blocks[index].y
			temparea=blocks[index].height*blocks[index].width
		if (index == 3) and (blocks[index].signature == 5):
			if (blocks[index].y > tempY):
				chestY=blocks[index].y
				chestarea=blocks[index].height*blocks[index].width
				HeadY=tempY
				Headarea=temparea
				tempY=0
			else:
				chestY=tempY
				HeadY=blocks[index].y
				tempY=0
#						

except (KeyboardInterrupt):
   api.ServoShutdown()
   sys.exit()