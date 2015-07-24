#!/usr/bin/env python
############################################################################################                                                                
#      EDITED BY DADILETTA   
# This script uses a ultrasonic sensor scan to identify a path forward
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
stopdistance = 50
fardistance = 80

def scan():
	stop()
	enable_servo()
	allclear = True
	for ang in range(30, 130, 2):
		servo(ang)
		time.sleep(.04)
		sweep[ang] = us_dist(15)
		print("Angle of", ang, "has distance", sweep[ang])
		if sweep[ang] < stopdistance:
			allclear = False
	return allclear

def turnto(ang):
	diff = 80 - ang
	turnboost = 1
	if abs(diff) > 30:
		turnboost = 2
		print "Need to turn more than 30 degrees. Boosting my turn."
	if diff >= 0:
		stop()
		print("Moving right.")
		enc_tgt(1,0,5*turnboost)
		right()
	else:
		stop()
		print("Moving left.")
		enc_tgt(0,1,5*turnboost)
		left()



while True:
	if scan() == True:
		stopcount = 0
		while True:
			servo(80)
			disable_servo()
			set_left_speed(120)
			set_right_speed(165)
			fwd()
			dist=us_dist(15)			#Find the distance of the object in front
			print "I see something ",dist,"cm ahead."
			if dist < stopdistance:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
				stopcount += 1
				print "Is that something in my way?"
			if stopcount > 2:
				print "Yup. Something in my way."
				stop() #Stop the GoPiGo
				break
	else:
		count = 0
		for ang in range(30, 130, 2):
			if sweep[ang] > fardistance:
				count += 1
			if count > 20:
				turnto(ang)
		if count < 20:
			print("I don't see a path ahead. I give up.")
			break

stop()
disable_servo()
