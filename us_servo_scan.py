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

keepgoing = True
sweep = [None] * 130
count = 0 
sdistance = 50 
edistance = 10

def scan():
	stop()
	for ang in range(30, 130, 2):
		servo(ang)
		time.sleep(.02)
		sweep[ang] = us_dist(15)
		print("Angle of", ang, "has distance", sweep[ang])
		if sweep[ang] < edistance:
			print("Stop signal sent. Close obstacle.")
			stop()

def findavector():
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
		keepgoing = False
		print("The while loop has now been set to", keepgoing)
	
def turnto(ang):
	diff = 80 - ang
	if diff >= 0:
		stop()
		right()
		time.sleep(diff/1000)
		stop()
	if diff < 0:
		stop()
		left()
		time.sleep(abs(diff)/1000)
		stop()

def rollon():
	for ang in range(30, 130, 2): 
		if sweep[ang] < sdistance:
			print("Problem detected. Calling findavector")
			findavector()
			break
		else:
			print("Path clear, moving forward")
			servo(80)
			fwd()

while keepgoing:
	print("Hi. While loop is set to", keepgoing)
	scan()
	rollon()
	if us_dist(15) < edistance:
		stop()
  
stop()
disable_servo()
