#!/usr/bin/env python
############################################################################################                                                                
#      EDITED BY DADILETTA                           
############################################################################################
#
# ! Attach Ultrasonic sensor to A1 Port.
#
############################################################################################
from gopigo import *
import sys
from collections import Counter
import math

sweep = [None] * 130
sdistance = 50

def scan():
	stop()
	allclear = True
	for ang in range(30, 130, 2):
		servo(ang)
		time.sleep(.02)
		sweep[ang] = us_dist(15)
		print("Angle of", ang, "has distance", sweep[ang])
		if sweep[ang] < sdistance:
			allclear = False
	return allclear

def turnto(ang):
	diff = 80 - ang
	
	if diff >= 0:
		stop()
		enc_tgt(1,0,4)
		right()
	else:
		stop()
		enc_tgt(0,1,4)
		left()



while True:
	if scan() == True:
		while True:
			dist=us_dist(15)			#Find the distance of the object in front
			print "Dist:",dist,'cm'
			if dist<sdistance:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
				print "Something in my way."
				stop() #Stop the GoPiGo
				break
	else:
		count = 0
		for ang in range(30, 130, 2):
			if sweep[ang] > sdistance:
				count += 1
			if count > 20:
				if ang < 80:
					print("Looks like I've got a path to the right.")
				else: 
					print("Looks like I've got a path to the left.")
				turnto(ang)
		if count < 20:
			print("I don't see a path ahead.")
			break

stop()
disable_servo()
