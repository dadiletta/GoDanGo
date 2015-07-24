#!/usr/bin/env python
########################################################################                                                                  
# This script uses an Ultrasonic sensor to detect a collision and turn right
#
########################################################################
#
# ! Attach Ultrasonic sensor to A1 Port.
#
########################################################################
from gopigo import *
import time
import sys
from collections import Counter
import math

distance_to_stop=30		#Distance from obstacle where the GoPiGo should stop
#TODO: Is my camera straight?


def FindPathRight(dist):
	while dist<distance_to_stop:
		stop()
		bwd()
		time.sleep(.5)
		stop()
		right_rot()
		time.sleep(.2)
		stop()
		dist=us_dist(15)			#Find the distance of the object in front
		print "Dist:",dist,'cm'
	print "Path is now clear, I think."


def trot():   #method to adjust the forward speed
	set_left_speed(120)
	set_right_speed(165)
	fwd()

print "Press ENTER to start"
raw_input()				#Wait for input to start
trot()					#Start moving
print "Weeeeeee"
while True:
	dist=us_dist(15)			#Find the distance of the object in front
	print "Dist:",dist,'cm'
	if dist<distance_to_stop:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
		print "Something in my way. Going to look for a new path"
		stop()					#Stop the GoPiGo
		FindPathRight(dist)
	print "Let's hit the road again."
	trot()


