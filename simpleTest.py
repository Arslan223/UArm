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

try:
	import vrep
	import keyboard
	import math
except:
	print ('--------------------------------------------------------------')
	print ('"vrep.py" could not be imported. This means very probably that')
	print ('either "vrep.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "vrep.py"')
	print ('--------------------------------------------------------------')
	print ('')

import time

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
		while True:
			arr = list(map(int, input().split()))
			try:
				setSignal('m1', arr[0])
				setSignal('m2', arr[1])
				setSignal('m3', arr[2])
				setSignal('m4', arr[3])
				setSignal('ch', 1)
				time.sleep(1)
				if arr[4] == 1:
					setSignal('gripOn', 1)
					setSignal('gripOff', 0)
				else:
					setSignal('gripOff', 1)
					setSignal('gripOn', 0)
				
				arr = []
			except:
			 	print("Error. Try Again.")
			 	continue
			if keyboard.is_pressed("q"):
				break


	except KeyboardInterrupt:
		rs = vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
		vrep.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
