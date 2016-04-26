#!/usr/bin/env python

# The following program is a text adventure game (IF) called
# "CIA", originally published as a BASIC program in the book
# "BASIC Fun With Adventure Games" by Susan Drake Lipscomb and
# Margaret Ann Zuanich (pub. by Avon Books, 1984, ISBN 0-380-87486-4).
#
# I decided to convert the game from BASIC over to Python, in order to
# learn the basics (no pun intended) of Python. The concept of the game
# belongs to the original authors, but the Python version I release to
# the public domain.
#
# Have fun, and I hope this helps you learn Python as much as it helped
# me. BTW - Mr. Bainbridge, if you read this - thanks for the book! Brent,
# Joe, and I say HI!

import os, random, sys, string, time
from string import *

rooms = []
help = []
commands = []
verbs = []
objects = []
directions = []
carried = []
words = []

def init():

	global room
	global time_elapsed
	global time_total
	global grim
	global vpos
	global npos
	
	print "Initializing..."
	print

	#

    	print "Reading room data...",
	
	f = open(os.path.join("rooms.dat"))
	lines = f.readlines()
	f.close()
	
	for line in lines:
		line = rstrip(line)
		
		if line[0:2] == '//': continue
		
		rooms.append(line)
		
	print "number of rooms: " + `len(rooms)`

	#

    	print "Reading help data...",
	
	f = open(os.path.join("help.dat"))
	lines = f.readlines()
	f.close()
    
	for line in lines:
		line = rstrip(line)
		
		if line[0:2] == '//': continue
		
		help.append(line)

	print "number of help entries: " + `len(help)`

	#

    	print "Reading command data...",
	
	f = open(os.path.join("commands.dat"))
	lines = f.readlines()
	f.close()
    
	for line in lines:
		line = rstrip(line)
		
		if line[0:2] == '//': continue
		
		commands.append(line)
		
	print "number of commands: " + `len(commands)`

	#

    	print "Reading verb data...",
	
	f = open(os.path.join("verbs.dat"))
	lines = f.readlines()
	f.close()
    
	for line in lines:
		line = rstrip(line)
		
		if line[0:2] == '//': continue
		
		verbs.append(line)
		
	print "number of verbs: " + `len(verbs)`

	#
	
	print "Reading object data...",
	
	f = open(os.path.join("objects.dat"))
	lines = f.readlines()
	f.close()
    
	for line in lines:
		line = rstrip(line)
		
		if line[0:2] == '//': continue
		
		objects.append(line)
		
	print "number of objects: " + `(len(objects)/3)`

	directions.append('north')
	directions.append('east')
	directions.append('south')
	directions.append('west')

	print "Intializing in-game variables..."
	
	room = 1
	time_elapsed = 0
	time_total = 1000
	grim = 0
	vpos = 0
	npos = 0
	
	print
	print ">>> DONE <<<"

def clrscr():

	for i in range(80):
		print

def showtitle():

	clrscr()

	print "Welcome to the game of..."
	print
	print "*******    ******     ***"
	print "*******    ******    *****"
	print "**           **     *** ***"
	print "**           **     **   **"
	print "**           **     **   **"
	print "**           **     *******"
	print "**           **     *******"
	print "**           **     **   **"
	print "**           **     **   **"
        print "**           **     **   **"
	print "*******    ******   **   **"
	print "*******    ******   **   **"

	time.sleep(5)	

def showinstr():

	print
	print "---"
	print
	print "You are a CIA agent. The department has just received"
	print "a tip that the Russian Ambassador, Vladimir Griminski"
	print "is passing classified information to the KGB."
	print
	print "You have two hours while the Ambassador is gone to collect"
	print "evidence of his crime. You start in your office and then"
	print "proceed to his apartment..."
	print
	print "Good luck on your mission, agent!"
	print
	
	key = raw_input("Press RETURN to start your mission")
	
	clrscr()
	
def newroom():

	global room
	
	print get_room_desc(room)

def getinput():

	global time_elapsed
	global time_total
	global words

	time_elapsed = time_elapsed + 3
	
	if time_elapsed > time_total:
		print "Sorry...you ran out of time..."
		sys.exit()
		
	words = split(raw_input(">> "))

def command():

	global words
	global room

	for c in range(len(commands)):
		if commands[c] == words[0]:
		        if c == 0:
				cmd_help()
				return
				
			if c == 1:
				cmd_quit()
				return
				
			if c == 2:
				cmd_inventory()
				return
				
			if c == 3:
				cmd_look()
				return
				
			if c == 4:
				cmd_time()
				return
				
			if c == 5:
				cmd_score()
				return
				
			if c == 6:
				cmd_restart()
				return
				
			if c == 7:
				cmd_verbs()
				return
			
			if c == 8:
				cmd_save()
				return
				
			if c == 9:
				cmd_restore()
				return
		
	print "I can't understand " + words[0]

def cmd_help():

	global room

	print help[room-1]

def cmd_quit():

	words = raw_input("Are you sure you want to quit? (yes, no) : ")
	
	if lower(words) <> "yes":
		print "Continuing..."
		return
	
	cmd_time()
	cmd_score()
	sys.exit()


def cmd_inventory():

	if len(carried) == 0:
		print "You aren't carrying anything..."
		return	
		
	print "You have:"
	
	for i in range(len(carried)):
		print get_oname(carried[i])
	
def cmd_look():
	
	global room
	
	print get_room_desc(room)

def cmd_time():

	global time_elapsed
	
	print "Elapsed time is " + `time_elapsed` + " minutes..."

def cmd_score():

	if len(carried) == 0:
		print "You aren't carrying anything..."
		return	
		
	score = 0		

	for i in range(len(carried)):
		score = score + get_otval(carried[i])

	print "Your current score is: " + `score`
	print
	print "Your rank is:"
	print
	
	srank = int(score / 10)
	
	if srank == 0:
		print "Amateur Sleuth - Go back for field training..."
		return
		
	if srank == 1:
		print "Intermediate Sleuth - Pound the beat some more..."
		return
		
	if srank == 2:
		print "Advanced Sleuth - You still need an assistant..."
		return
		
	if srank == 3:
		print "Expert Operative - You can handle any mission alone..."
		return
		
	if srank == 4:
		print "World Renowned Operative - You will be elevated to control..."
		return
	
	#print "You have " + `score` + " points for evidence..."

def cmd_restart():

	words = raw_input("Are you sure you want to restart? (yes, no) : ")
	
	if lower(words) == "yes":
		init()
		clrscr()
		newroom()
		return
	
	print "Continuing..."
	
def cmd_verbs():

	print
	print "I can understand the following verbs:"

	for v in range(len(verbs)):
		print verbs[v]
	

def cmd_save():

	f = open(os.path.join("savegame.dat"), "w")

	f.write(str(room) + "\n")
        f.write(str(time_elapsed) + "\n")
	f.write(str(grim) + "\n")
	
	f.write(str(len(rooms)) + "\n")
	for line in range(len(rooms)):
		f.write(rooms[line] + "\n")
		
	f.write(str(len(objects)) + "\n")
	for line in range(len(objects)):
		f.write(objects[line] + "\n")

	f.write(str(len(carried)) + "\n")
	for line in range(len(carried)):
		f.write(str(carried[line]) + "\n")
			
	f.close()
	
	print "Game saved..."

def cmd_restore():

	global room
	global grim
	global time_elapsed
	
	if os.path.exists(os.path.join("savegame.dat")):
		f = open(os.path.join("savegame.dat"))
		lines = f.readlines()
		f.close()

		if len(lines) > 0:
			room = int(rstrip(lines[0]))
			time_elapsed = int(rstrip(lines[1]))
			grim = int(rstrip(lines[2]))

			count_range = int(rstrip(lines[3]))
	        	pos = 4
			for num in range(count_range):
				rooms[num] = rstrip(lines[pos])
				pos += 1

			count_range = int(rstrip(lines[pos]))
			pos += 1
			for num in range(count_range):
				objects[num] = rstrip(lines[pos])
				pos += 1

			count_range = int(rstrip(lines[pos]))
			pos += 1
			for num in range(count_range):
				carried.append(int(rstrip(lines[pos])))
				pos += 1
			
			print "Game restored..."
			
			time.sleep(2)
			clrscr()
			cmd_look()
			
		else:
			print "Invalid game save file, unable to restore..."
		
	else:
		print "Game not saved, unable to restore..."

def parse():

	global room
	global vpos
	global npos
	
	for vpos in range(len(verbs)):
		if verbs[vpos] == words[0]:
			vpos += 1

			for npos in range(len(objects)):
				ob_name = lower(get_oname(npos+1))
				
				if ob_name == words[1]:
					if get_oroom(npos+1) == room or get_oroom(npos+1) == 100:
						npos += 1
						return

			print "It won't help..."
			npos = 0
			return
					
	vpos = 0
	
	print "I don't know how to " + words[0]
	
def action():

	global vpos
	global npos

	ob_name = lower(get_oname(npos))

	if get_otcod(npos) == 2:
		print "You can't " + words[0] + " " + words[1] + " yet..."
		return
	
        if vpos == 1:
		vrb_look()
		return
				
	if vpos == 2 or vpos == 3:
		vrb_take()
		return
				
	if vpos == 4 or vpos == 5 or vpos == 6:
		vrb_go()
		return
		
	if vpos == 7:
		vrb_open()
		return
		
	if vpos == 8:
		vrb_read()
		return
		
	if vpos == 9:
		vrb_drop()
		return
	
	if vpos == 10:
		vrb_call()
		return
		
	if vpos == 11:
		vrb_unscrew()
		return

	if vpos == 12:
		vrb_spray()
		return
		
	if vpos == 13:
		vrb_push()
		return
		
	if vpos == 14:
		vrb_load()
		return
		
	if vpos == 15:
		vrb_run()
		return
		
	if vpos == 16:
		vrb_drink()
		return
		
	if vpos == 17 or vpos == 18:
		vrb_eat()
		return
		
	if vpos == 19:
		vrb_unwrap()
		return
	
	if vpos == 20:
		vrb_talk()
		return
				
	if vpos == 21:
		vrb_shoot()
		return
		
	if vpos == 22:
		vrb_unlock()
		return
		
	if vpos == 23:
		vrb_on()
		return
		
	if vpos == 24:
		vrb_off()
		return
		
	print "Action!"

def vrb_look():

	global npos
	global room
	
	ob_desc = get_odesc(npos)

	print ob_desc

       	ob_link = get_olink(npos)
	
	while(ob_link <> 0):
		npos = ob_link

       		ob_link = get_olink(npos)

		if get_oroom(npos) == room:
			print get_odesc(npos)
	
def vrb_take():

	global npos
	global room

	ob_name = get_oname(npos)
	ob_room = get_oroom(npos)
	ob_take_code = get_otcod(npos)

	if ob_take_code == 1:
		if len(carried) < 6:
			if ob_room == 100:
				print "You already have it..."
				return
			
			print "Taken..."
			
			set_oroom(npos, 100)
			carried.append(npos)
			
		else:
		  print "You can't carry anything else..."
		  
	if ob_take_code == 2 or ob_take_code == 5:
		print "You can't take the " + ob_name + " yet."
		
	if ob_take_code == 3:
		print "It is too heavy to carry..."
		
	if ob_take_code == 4:
		print "That's ridiculous!"
	
def vrb_go():

	global npos
	global room

	for j in range(4):
		if directions[j] == words[1]:
			room_info = split(rooms[room-1], "~")

			if int(room_info[j+1]) <> 0:
				room = int(room_info[j+1])
				newroom()
				return	  
			
	print "I can't go that direction..."

def vrb_open():

	global npos

	if npos == 12:
		if get_otcod(12) == 4 and get_otcod(13) == 4:
			print "Opened..."
			set_room_exit(2,1,3)
			return
			
		if get_otcod(12) == 5:
			print "The door is locked..."
			return
			
		if get_otcod(13) == 5:
			print "You didn't disconnect the alarm. It goes off, and the police come to arrest you...END OF GAME!"
			sys.exit()

		print "You are unable to open the door..."
		return			
		
	if npos == 18:
		combo = raw_input("Combination? :")

		if combo == "2-4-8":
			print "Opened..."
			set_odesc(18,"There is a black leather briefcase with a combination lock. Parts of an RR-13 rifle are inside the padded case.")
			return
		
		print "The combination doesn't open it..."

	if npos == 44:
		combo = raw_input("Combination? :")

		if combo == "20-15-9":
			print "Opened..."
			set_olink(44, 45)
			set_otcod(45, 1)			
			set_odesc(44,"This is a standard combination safe. Inside is:")
			return
		
		#print "The combination doesn't open it..."
		
		if combo <> "":
			print
			print "You've had it!"
			print
			print "The safe is boobie trapped and explodes!!!"
			print "END OF GAME"
			sys.exit()

	if npos == 49:
		print "Opened..."
		set_olink(49, 51)
		set_otcod(51, 1)			
		set_room_desc(10,"You are in a combined bathroom and dressing area. The Ambassador's clothes are hanging neatly on rods and open shelves hold towels and sweaters. The medicine cabinet is open.")
		return

	if npos == 17:
		print "You stab yourself with the tip, which is a poisoned dart. You are rushed to the hospital...END OF GAME!"
		sys.exit()

	if npos == 21:
		print "Opened..."
		set_olink(21, 57)
		set_otcod(57, 1)			
		return

	if npos == 37:
		print "Opened..."
		set_olink(37, 38)
		set_otcod(38, 1)			
		set_room_desc(8,"You are in the apartment kitchen which shimmers with polished chrome appliances and buther block counters. A long cabinet above the stainless steel sinks is open. A freezer stands in the corner.")
		return

	if npos == 60:
		print "Opened..."
		set_odesc(60,"This is a small white freezer. Inside are containers of frozen yogurt, caviar, and frozen herring. A box sitting on the rack on the door is labeled 'FILM'...")
		return
			
	ob_name = lower(get_oname(npos))

	print "The " + ob_name + " can't be opened..."

def vrb_read():

	global npos
	global room

	if room == 3 and npos == 16:
		print "The telephone bill is made out to 322-9678 - V.GRIM, P.O. Box 2023, Grand Central Station, NYC. The amount is $247.36 for long distance charges to Washington, DC..."
		return
		
	if npos == 20:
		print "You can just make out this message: HEL-ZXT.93.ZARF.1"
		return
		
	if npos == 23:
		print "The bill is made out to  322-8721 - Ambassador Vladimir Griminski, 14 Parkside Avenue, NYC. The bill is for $68.34 for mostly local calls..."
		return
	
	if npos == 25:
		print "322-8721"
		return
	
	if npos == 30:
		print "322-9678"
		return
	
	if npos == 42:
		print "20-15-9"
		return
		
	if npos == 56:
		print "322-8721"
		return
		
	print "Nothing to read..."
	
def vrb_drop():

	global npos
	global room
	
	for i in range(len(carried)):
		if npos == carried[i]:
			print "Dropped..."
			set_oroom(carried[i], room)
			carried.remove(npos)
			return

	ob_name = lower(get_oname(npos))

	print "You aren't carrying a " + ob_name

def vrb_call():

	global npos
	global room
	global time_elapsed
	global time_total

	if npos == 53 and (room == 5 or room == 6 or room == 9):
		print "Ring...Ring..."
		print "Hello, agent. This is your control speaking."
		print "Please list your tangible evidence (enter a blank to stop listing evidence):"
		
		EV = 0
		ev_list = []
		
		while (1):
			ev_object = raw_input("-> ")

			if ev_object == "": break
			
			found = 0
			
			for i in range(len(carried)):
				if lower(ev_object) ==	lower(get_oname(carried[i])):
					found = 0

					for j in range(len(ev_list)):
						if ev_list[j] == carried[i]:
							found = 1
							print "You already said " + ev_object + "..."
							
					if found == 0:
						EV += get_otval(carried[i])
						ev_list.append(carried[i])
						found = 1
			
			if not found:
				print "You are not carrying a " + ev_object
			
		if EV >= 40:
			print "Fantastic job!"
			print "We'll be over immediately to arrest the suspect!"

			time_elapsed = time_elapsed + 6
	
			if time_elapsed > time_total:
				getinput()
				return

			print "-------------"
			print "Ambassador Griminski arrives home at 10:30 to find operatives waiting to arrest him."
			print "-------------"
			print "You are handsomely rewarded for your clever sleuthing."
			print "You solved the mystery in " + str(time_elapsed) + " minutes..."
			sys.exit()
		
		print "I'm sorry...you have insuficient evidence for a conviction. Call me back when you have more information..."
		return

	if npos <> 53:
		print "It's no use to call " + words[1]
		return
		
	print "You're not near a phone..."
	return

def vrb_unscrew():

	global npos

	if npos == 13:
		for i in range(len(carried)):
			if lower(get_oname(carried[i])) == "screwdriver":
				print "The alarm system is off."
				set_otcod(13, 4)			
				set_odesc(13,"The alarm is disabled.")
				return
			
		print "You have nothing to unscrew with..."
		return

	print "You can't unscrew a " + words[1]

def vrb_spray():

	global npos
	global words
	
	if npos == 14 or npos == 10:
		for i in range(len(carried)):
			if carried[i] == 10:
				print "The dog is drugged and falls harmlessly at your feet..."
				
				set_room_exit(3,1,5)
				set_room_exit(3,2,9)
				set_room_exit(3,4,4)
		
				set_room_desc(3,"This is the marbled foryer of the Ambassador's apartment. There is a table in the corner. The master bedroom is east, the drawing room is north, and a closet is west. The drugged dog is on the floor.")
				set_odesc(14,"The fierce doberman lies drugged on the floor.")
				carried.remove(10)

				print "The drug is used up and is no longer in your inventory."
				return
				
		print "You have nothing to spray with..."
		return
	
	print "You can't spray a " + words[1]
	
def vrb_push():

	global npos
	
	if npos == 26:
		print "The panel pops open to reveal the entrance to a previously hidden room..."
		set_room_exit(5,2,6)
		set_odesc(26,"The panels are tongue-in-groove. A hidden room can be seen behind one panel.")
		return
	
	print "It doesn't do any good to puch a " + words[1]
	
def vrb_load():

	global npos
	
	if npos == 28:
		if get_oroom(28) == 6:
			print "The program is already loaded..."
			return
			
		print "That won't help you..."

	print "You can't load a " + words[1]
	
def vrb_run():

	global npos
	global grim
	
	if npos == 28:
		if get_otcod(31) == 5 or get_otcod(32) == 5 or get_otcod(33) == 5:
			print "The computer can't run the program yet..."
			return
		
		set_otcod(28,1)

		print "The program dials a Washington, DC number. A message appears on the monitor:"
		print
 		
		passw = raw_input("Please login: ")

		if passw == "HEL-ZXT.93.ZARF.1":
			print "The following message appears on the monitor:"
			print
			print "This is the US DOD Top Secret account for weapons development and stealth aircraft data. All information is classified..."
			return
			
		if grim == 0:
			grim = 2
			print
			print "Invalid login code - connection closed. (the screen goes blank)"
			print
			print "You hear footsteps..."
			print "Griminski looms in the doorway with an 8mm Lugar in-hand. You'd better have brought the PPK-3 pistol from the department or you're finished!"
			
			getinput()
			
			if len(words) == 0:
				print "It's hopeless! Griminski fires his gun, and you crumple to the floor..."
				print "END OF GAME"
				sys.exit()
				
			parse()
			
			if lower(words[0]) == "shoot" and (npos == 8 or npos == 58):
				vrb_shoot2()
			
			return
		
		print "Invalid login code - connection terminated."
		return
	
	print "You can't run a " + words[1]
	
def vrb_drink():

	global npos
	global words
	
	if npos == 36:
		print "You are poisoned. Staggering to the phone, you call an ambulance, and wait for it to arrive..."
		print "END OF GAME"
		sys.exit()
	
	print "You can't drink the " + words[1] + "..."
	
def vrb_eat():

	global npos
	global words
	
	if npos == 39 or npos == 54:
		print "You fool! These are cyanide capsules! You are poisoned, and fall writhing to the floor, dying in agony..."
		print "END OF GAME"
		sys.exit()
		
	if npos == 45:
		print "You idiot! The 'gum' is a plastic explosive - you have just blown yourself to smithereens!!"
		print "END OF GAME"
		sys.exit()
	
	print "You can't " + words[0] + " the " + words[1] + "..."
	
def vrb_unwrap():

	global npos
	
	if npos == 45:
		print "The wrapper conceals a tiny strip of microfilm..."
		set_otcod(46,1)
		return

	print "It doesn't help to unwrap " + words[1]
		
def vrb_talk():

	global npos
	
	if npos == 14:
		print "He doesn't speak english!"
		return
	
	print "That won't help you..."
	
def vrb_shoot():

	global npos
	
	if npos == 8 or npos == 14 or npos == 58:
		vrb_shoot2()
		return
	
	print "That won't help!"

def vrb_shoot2():

	global npos
	global grim
	global room
	
	for i in range(len(carried)):
		if carried[i] == 8:
			if room == 3 and (npos == 8 or npos == 14):
				print "The dog bites your hand!"
				return
			
			if room <> 6:
				print "That just makes a big mess!"
				return
				
			if grim <> 2:
				print "That won't help!"
				return
		
			print "Your shot grazes his forehead. He crashes to the floor unconcious. You have time to gather additional evidence to apprehend him."
			grim = 1
			set_room_desc(6,"You can see a microcomputer and phone modem and monitor on a table against the east wall of this over-sized closet. A phone is by the computer. A chair and shelves are here. Griminski is lying unconcious on the floor.")
			return
			
	if room == 6 and grim == 2:
		print "You don't have the pistol - anything else takes too much time!"
		return
		
	print "You have nothing to shoot with..."

def vrb_unlock():

	global npos
	
	if npos == 12:
		for i in range(len(carried)):
			if lower(get_oname(carried[i])) == "key":
				print "You unlock the door with the key..."
				set_otcod(12,4)
				return
			
		print "You have nothing to unlock the door with..."
		return
	
	print "You can't " + words[0] + " a " + words[1] + "..."

def vrb_on():

	global npos
	
	if npos >= 31 and npos <= 33:
		if npos == 31:
			set_odesc(31,"This is a standard business type of microcomputer with a keyboard and a program in one of the disk drives. The on/off switch is on.")

		if npos == 32:
			set_odesc(32,"This is a hi-res color monitor. The on/off switch is on.")
			
		if npos == 33:
			set_odesc(33,"The phone modem is one that can use an automatic dialing communications program. The on/off switch is on.")
		
		print "On"
		set_otcod(npos,3)
		return
	
	print "You can't turn on a " + words[1]

def vrb_off():

	global npos
	
	if npos >= 31 and npos <= 33:
		if npos == 31:
			set_odesc(31,"This is a standard business type of microcomputer with a keyboard and a program in one of the disk drives. The on/off switch is off.")

		if npos == 32:
			set_odesc(32,"This is a hi-res color monitor. The on/off switch is off.")
			
		if npos == 33:
			set_odesc(33,"The phone modem is one that can use an automatic dialing communications program. The on/off switch is off.")
		
		print "Off"
		set_otcod(npos,5)
		return
	
	print "You can't turn off a " + words[1]

def get_oname(obnum):

	return split(objects[obnum-1], "~")[0]
	
def get_odesc(obnum):

	return split(objects[obnum-1], "~")[1]

def set_odesc(obnum, value):

	ob_info = split(objects[obnum-1], "~")

	objects[obnum-1] = str(ob_info[0]) + "~" + str(value) + "~" + str(ob_info[2]) + "~" + str(ob_info[3]) + "~" + str(ob_info[4]) + "~" + str(ob_info[5])

def get_oroom(obnum):

	ob_attrs = split(objects[obnum-1], "~")
	return int(ob_attrs[2])

def set_oroom(obnum, value):

	ob_info = split(objects[obnum-1], "~")

	objects[obnum-1] = str(ob_info[0]) + "~" + str(ob_info[1]) + "~" + str(value) + "~" + str(ob_info[3]) + "~" + str(ob_info[4]) + "~" + str(ob_info[5])

def get_olink(obnum):

	ob_attrs = split(objects[obnum-1], "~")
	return int(ob_attrs[3])

def set_olink(obnum, value):

	ob_info = split(objects[obnum-1], "~")

	objects[obnum-1] = str(ob_info[0]) + "~" + str(ob_info[1]) + "~" + str(ob_info[2]) + "~" + str(value) + "~" + str(ob_info[4]) + "~" + str(ob_info[5])
	
def get_otval(obnum):

	ob_attrs = split(objects[obnum-1], "~")
	return int(ob_attrs[4])

def get_otcod(obnum):

	ob_attrs = split(objects[obnum-1], "~")
	return int(ob_attrs[5])

def set_otcod(obnum, value):

	ob_info = split(objects[obnum-1], "~")

	objects[obnum-1] = str(ob_info[0]) + "~" + str(ob_info[1]) + "~" + str(ob_info[2]) + "~" + str(ob_info[3]) + "~" + str(ob_info[4]) + "~" + str(value)

def set_room_exit(rmnum, dirv, link):

	room_info = split(rooms[rmnum-1], "~")
	
	room_info[dirv] = link

	rooms[rmnum-1] = room_info[0] + "~" + str(room_info[1]) + "~" + str(room_info[2]) + "~" + str(room_info[3]) + "~" + str(room_info[4])

def get_room_desc(rmnum):

	return split(rooms[rmnum-1], "~")[0]

def set_room_desc(rmnum, desc):
	
	room_info = split(rooms[rmnum-1], "~")

	rooms[rmnum-1] = desc + "~" + str(room_info[1]) + "~" + str(room_info[2]) + "~" + str(room_info[3]) + "~" + str(room_info[4])

def main():

	global vpos
	global npos
	global words
	
	init()
	showtitle()
	showinstr()
	newroom()
	
	while(1):
		getinput()
	
		if len(words) > 0:
			if len(words) == 1:
				command()
			else:
				parse()
				if (vpos <> 0 and npos <> 0):
					action()

if __name__ == '__main__': main()
