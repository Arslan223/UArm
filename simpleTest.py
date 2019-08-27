# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!





def setSignal(name, value):
	rs = vrep.simxSetIntegerSignal(clientID, name, value, vrep.simx_opmode_oneshot_wait)

import vrep, time, sys, array, keyboard, math, cv2, numpy
from PIL import Image as I
import matplotlib.pyplot as plt
from threading import Thread
import sys
import speech_recognition as sr


def getInput():
	r = sr.Recognizer()

	with sr.Microphone() as source:
		audio = r.listen(source)

		try:
			text = r.recognize_google(audio)
			print(text)
			return text
		except:
			print('Couldnt recognize')

def armMotor(arr):
	setSignal('m1', arr[0])
	setSignal('m2', arr[1])
	setSignal('m3', arr[2])
	setSignal('m4', arr[3])
	setSignal('ch', 1)
	if arr[4] == 1:
		setSignal('gripOn', 1)
		setSignal('gripOff', 0)
	else:
		setSignal('gripOff', 1)
		setSignal('gripOn', 0)
	if arr[5] == 1:
		setSignal('gripOn1', 1)
		setSignal('gripOff1', 0)
	else:
		setSignal('gripOff1', 1)
		setSignal('gripOn1', 0)

def armMotion():
	while True:
		try:
			a = getInput()
			ch = False
			if a == 'water':
				arr = [[90, 104, 60, 90, 0, 0], [90, 150, 60, 90, 0, 0], [6, 150, 60, 90, 0, 0], [6, 122, 65, 90, 0, 0], [6, 122, 65, 90, 0, 1], [6, 122, 10, 90, 0, 1], [6, 104, 10, 90, 0, 1], [90, 115, 10, 90, 0, 1], [90, 115, 10, 90, 0, 0]]
				ch = True
			elif a == 'money':
				arr = [[180, 104, 60, 90, 1, 0], [180, 55, 92, 90, 1, 0], [180, 104, 60, 90, 1, 0], [90, 104, 60, 90, 1, 0], [90, 104, 60, 90, 0, 0]]
				ch = False
			else:
				continue
			for i in range(len(arr)):
				armMotor(arr[i])
				time.sleep(3)
			arr = []
			if ch:
				er, btl = vrep.simxGetObjectHandle(clientID, "Shape", vrep.simx_opmode_oneshot_wait)
				er = vrep.simxSetObjectPosition(clientID, btl, -1, (0,0,0), vrep.simx_opmode_oneshot_wait)
			else:
				er, btl = vrep.simxGetObjectHandle(clientID, "uarm_pickupPart", vrep.simx_opmode_oneshot_wait)
				er = vrep.simxSetObjectPosition(clientID, btl, -1, (0,0,0), vrep.simx_opmode_oneshot_wait)

		except:
			sys.exit(0)
	
		

def showV1():
	while True:
		try:
			res, v0 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
			res, v1 = vrep.simxGetObjectHandle(clientID, 'v1', vrep.simx_opmode_oneshot_wait)
			err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
		except EOFError:
			break
		if err == vrep.simx_return_ok:
			image_byte_array = array.array('b', image).tobytes()
			image_buffer = I.frombuffer("RGB", (1024, 1024), image_byte_array, "raw", "RGB", 0, 1)
			img2 = numpy.asarray(image_buffer)


				#--------

			img2 = img2.ravel()
			vrep.simxSetVisionSensorImage(clientID, v1, img2, 0, vrep.simx_opmode_oneshot)

def streamVisionSensor(visionSensorName,clientID,pause=0.0001):
	#Get the handle of the vision sensor
	#Give a title to the figure
	res, v0 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
	res, v1 = vrep.simxGetObjectHandle(clientID, 'v1', vrep.simx_opmode_oneshot_wait)
	#Let some time to Vrep in order to let him send the first image, otherwise the loop will start with an empty image and will crash
	arr = [90, 104, 60, 90, 0, 0]
	

	err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
	time.sleep(1)
	th_1, th_2 = Thread(target=showV1), Thread(target = armMotion)
	if (__name__ == '__main__')&(vrep.simxGetConnectionId(clientID)!=-1):
		th_1.start(), th_2.start()
		th_1.join(), th_2.join()
			
	print ('End of Simulation')
print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
	print ('Connected to remote API server')

	try:
		setSignal('m1', 90)
		setSignal('m2', 104)
		setSignal('m3', 60)
		setSignal('m4', 90)
		setSignal('ch', 1)
		streamVisionSensor("Vision_sensor", clientID)
	except KeyboardInterrupt:
		rs = vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
		vrep.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')