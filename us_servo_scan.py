#!/usr/bin/env python
############################################################################################                                                                
#      EDITED BY DADILETTA   : http://lancertechga.org
# This script uses a ultrasonic sensor scan to identify a path forward
############################################################################################
#
# Reference GoPiGo commands at: http://www.dexterindustries.com/GoPiGo/programming/python-programming-for-the-raspberry-pi-gopigo/
# ! Attach Ultrasonic sensor to A1 Port.
#
############################################################################################
from gopigo import *
import sys  #Used to get input from user via console
from collections import Counter  #do I even need this?
import math  #Do I need this?

sweep = [None] * 160  #the list to hold scanning data
stopdistance = 50  #distance at which the vehicle will halt or will trigger an unsafe scan
fardistance = 80  #distance used when plotting a clear direction... longer so we're planning farther ahead

def scan():
	stop()  #I tried making it scan while in motion but couldn't manage it.. is this impossible with the GoPiGo?
	enable_servo()  #I don't think I need to enable this. Can I remove?
	allclear = True
	print "Starting to scan."
	for ang in range(10, 160, 2): #wide scan, skipping all the odd numbers to move quicker
		servo(ang)  #move the servo to the angle in the loop
		time.sleep(.09) #pause between scans seems to get better results (has to be before the sensor is activated)
		sweep[ang] = us_dist(15) #note the distance at each angle
		print("Angle of", ang, "has distance", sweep[ang])
		if sweep[ang] < stopdistance and ang > 65 and ang < 95: #if we detect any obstacle in the direct path ahead
			allclear = False
	return allclear

def turnto(ang):
	#TODO: Debug, sometimes not turning, sometimes turning excessively
	diff = 80 - ang  #for some reason, 80 degrees is straight ahead with my servo
	turnboost = 1
	if abs(diff) > 30: #greater than 30 degrees, we should increase the amount needed to turn
		turnboost = 2
		print "Need to turn more than 30 degrees. Boosting my turn."
	if diff >= 0:
		stop()
		print("Moving right.") 
		enc_tgt(1,0,(5*turnboost)) #18 is a full rotation of the wheel, 
		right()
		time.sleep(.5) #give the bot time to turn before the app moves on
	else:
		stop()
		print("Moving left.")
		enc_tgt(0,1,(5*turnboost)) 
		left()
		time.sleep(.5) #give the bot time to turn before the app moves on

def turnaround():
	command = raw_input().lower() #take a command and make it lowercase
	if command == "yes" or command == "y" or command == "sure":
		stop()
		servo(80)
		disable_servo()
		print "Backing up. Beep beep beep."
		bwd()   #TODO: Why doesnt this back up? Mostly just rotates.
		time.sleep(.8)  #TODO: Replace sleeps with enc_tgt. Was having trouble with it.
		stop()
		right_rot()
		time.sleep(.8)
		stop()
		return True
	else:
		return False #user said not to continue. Return false and break the loop

#HERE'S WHERE THE PROGRAM STARTS
while True:
	if scan() == True:   #Call the scan and if allclear returns positive, let's roll
		stopcount = 0 #avoids false stops by having to detect an obstacle multiple times
		print "Let's roll."   #always good to print messages so you can debug easier
		while True:
			#TODO: Can I script a volt meter so if there are any spikes we stop for that as well?
			#TODO: servo sometimes twitches while driving. Why? I disable it... 
			servo(80)  #move the sensor straight ahead, happens to be 80 for my servo
			disable_servo()
			set_left_speed(120)  #adjust these so your GoPiGo cruises straight
			set_right_speed(145) #adjust these so your GoPiGo cruises straight
			fwd()
			dist=us_dist(15)			#Find the distance of the object in front
			print "I see something ",dist,"cm ahead."
			if dist < stopdistance:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
				stopcount += 1
				print "Is that something in my way?"
			if stopcount > 2:
				print "Yup. Something's in my way."
				stop() #Stop the GoPiGo
				break #stop the fwd loop
	else:   #here's where we find a safe window to drive forward
		count = 0  #
		for ang in range(10, 160, 2):
			if sweep[ang] > fardistance:
				count += 1   #count how many angles have a clear path ahead
			else: 
				count = 0   #resets the counter to 0 if a obstacle is detected, we only want 20 returns of safe in a row
			if count >= 15:   #15 counts means 30 degrees (since I count by 2s in the loop)
				turnto(ang)
				break #once we've found a path, stop looping through the scan data. This favors the right side since that's scanned first
		if count < 15:     #This is what happens if a window of obstacle-free scan data is not found
			print("I don't see a path ahead. Shall I try a 180?")
			if not turnaround(): #if turnaround returns false
				break #shut it down if ya can't turn 'round

stop()   #once the loop is broken, let's tidy things up just to be sure.
disable_servo()
