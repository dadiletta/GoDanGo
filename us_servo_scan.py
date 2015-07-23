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
	for ang in range(30, 130, 2):
		servo(ang)
		time.sleep(.02)
		sweep[ang] = us_servo(15)
		if sweep[ang] < edistance:
			print("EMERGENCY STOP")
			stop()

def pscan():
	for ang in range(30, 130, 2):
		print("Angle of", ang, "has distance", sweep[ang])

def rollon():
	for ang in range(30, 130, 2): 
		if sweep[ang] < sdistance:
			print("Problem detected. Calling findavector")
			findavector()
			break
		else:
			print("Path clear, moving forward")
			fwd()


def findavector():
	count = 0
	for ang in range(30, 130, 2):
		if sweep[ang] > ddistance:
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

while keepgoing:
	scan()
	pscan()
	rollon()
  
stop()
disable_servo()
