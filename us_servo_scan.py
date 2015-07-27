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
stopdistance = 50  #distance at which the vehicle will halt while in motion
fardistance = 90  #distance used when plotting a clear direction... longer so we're planning farther ahead

def quickcheck():
	servo(65)  #check the right edge of our forward path
	time.sleep(.07) #pause so the sensor reading is more accurate
	check1 = us_dist(15) #first check
	servo(80)  #check dead ahead
	time.sleep(.07)
	check2 = us_dist(15)
	servo(95) #check the left edge of our forward path
	time.sleep(.07)
	check3 = us_dist(15)
	if check1 > fardistance and check2 > fardistance and check3 > fardistance:
		print "Quick check looks good."
		return True
	else:
		return False

def scan():
	while stop() == 0:  #bot sometimes doesn't stop, so I loop the command until it returns a 1 for completed
		print "Having trouble stopping"
	allclear = True
	if not quickcheck():
		print "Starting a full scan."
		for ang in range(10, 160, 2): #wide scan, skipping all the odd numbers to move quicker
			servo(ang)  #move the servo to the angle in the loop
			time.sleep(.07) #pause between scans seems to get better results (has to be before the sensor is activated)
			sweep[ang] = us_dist(15) #note the distance at each angle
			print "[Angle:", ang, "--", sweep[ang], "cm]"
			if sweep[ang] < fardistance and ang > 65 and ang < 95: #if we detect any obstacle in the direct path ahead
				allclear = False
	return allclear

def turnto(ang):   #first calculate whether to use a low/med/high turn, then execute the turn
	while stop() == None:  #stop loop to prepare for turn
			print "Having trouble stopping"
	diff = 80 - (ang-15)  #for some reason, 80 degrees is straight ahead with my servo. I take off 15 from ang to find the center of the window
	turnnum = 5  #reset the turn num to default value
	if abs(diff) > 30 and abs(diff) <= 60: #greater than 30 degrees, we should increase the amount needed to turn
		turnnum = 10
		print "Setting turn variable to 10."
	elif abs(diff) > 60:
		turnnum = 15
		print "Setting turn variable to 15."
	else:
		print "Setting turn variable to 5."
	if diff >= 0:
		enc_tgt(1,0,turnnum)
		print "Moving right. Command returned:", right(),"message"
	else:
		enc_tgt(0,1,turnnum) 
		print "Moving left. Command returned:", left(),"message"
	time.sleep(1)  #give it a second...
	while stop() == None:
		print "Having trouble stopping"

def voltcheck():  #this check runs at the top of the main while loop
	if volt() < 7:
		print "Not enough power"
		return False
	elif volt() > 12:
		print "Spike in voltage!"
		return False
	else:
		print "Power is", volt(), "V"
		return True

def turnaround():
	while stop() == None:
		print "Having trouble stopping"
	print "Backing up. Beep beep beep."
	while bwd() == None:
		print "Having trouble backing up"
	time.sleep(.8)  #TODO: Replace sleeps with enc_tgt. Was having trouble with it.
	while stop() == None:
		print "Having trouble stopping"
	right_rot()
	time.sleep(.8)
	while stop() == None:
		print "Having trouble stopping"

#HERE'S WHERE THE PROGRAM STARTS
while voltcheck():  #keep looping as long as the power is within acceptable range
	if scan() == True:   #Call the scan and if allclear returns positive, let's roll
		stopcount = 0 #avoids false stops by having to detect an obstacle multiple times
		print "Let's roll."   #always good to print messages so you can debug easier
		while True:
			#TODO: servo sometimes twitches while driving. Why? I disable it... 
			servo(80)  #move the sensor straight ahead, happens to be 80 for my servo
			while disable_servo() == None:
				print "Having trouble disabling my servo"
			set_left_speed(120)  #adjust these so your GoPiGo cruises straight
			set_right_speed(155) #adjust these so your GoPiGo cruises straight
			fwd()
			dist=us_dist(15)			#Find the distance of the object in front
			print "Obj",dist,"cm."
			if dist < stopdistance:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
				stopcount += 1
				print "Is that something in my way?"
			if stopcount > 2:
				print "Yup. Something's in my way."
				while stop() == None:
					print "Having trouble stopping"
				break #stop the fwd loop
	else:   #here's where we find a safe window to drive forward
		count = 0  #counter to track the number of safe angles in a row
		for ang in range(10, 160, 2):
			if sweep[ang] > fardistance:
				count += 1   #count how many angles have a clear path ahead
			else: 
				count = 0   #resets the counter to 0 if a obstacle is detected, we only want counts in a row
			if count >= 10:   #10 counts means 20 degrees (since I count by 2s in the loop)
				turnto(ang)
				break #once we've found a path, stop looping through the scan data. This favors the right side since that's scanned first
		if count < 10:     #This is what happens if a window of obstacle-free scan data is not found
			print "I don't see a path. [S]can again | [T]urn around | [Q]uit"
			command = raw_input().lower() #take a command and make it lowercase
			if command == "s" or command == "scan":
				continue
			elif command == "t" or command == "turn":
				turnaround()
			else:	
				break

stop()   #once the loop is broken, let's tidy things up just to be sure.
disable_servo()
