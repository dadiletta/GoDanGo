#!/usr/bin/env python
########################################################################                                                                  
# This example demonstrates using the Ultrasonic sensor with the GoPiGo
#
# In this examples, the GoPiGo keeps reading from the ultrasonic sensor and when it close to the an obstacle, it stops.
#
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
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


