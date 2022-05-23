# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re

inputfile = open("zuerichstammtischarchiv.txt","r")

issamesession = 0
datestring = ""
message = ""
nachricht = ""
timeoflastmessage = datetime.strptime('00:00', '%H:%M').time() 
timeofmessage = datetime.strptime('00:00', '%H:%M').time()
dateofmessage = datetime.now()
sender = ""

newline = ""
protokoll = ""
edition = ""
editiontype = ""
place = ""
attendees = ""


for line in inputfile: 
	if line.startswith("==="):
	
		if (protokoll!=""):
			newline = newline + '\t' + protokoll + "\n"
			with open('zuerichtreffen.txt', 'a') as output:
				output.write(newline)
			protokoll = ""
		
		editiontype = re.search("=== .*? •", line).group(0)[4:-3]
		if re.match("[0-9]+.", editiontype):
			edition = re.search("=== [0-9]+.", line).group(0)[4:-1]
		editiontype = editiontype.replace(edition + ". ","")
		if re.search("in", line):
			place = re.search("in .*", line).group(0)[3:-4]
			place = place.replace("[[", "").replace("]]", "")
			if re.search("|", place):
				find = re.compile(r"^[^|]*")
				place = re.search(find, place).group(0)
				
		datestring = re.search("•.* ===", line).group(0)[4:-4]
		datestring = re.search("(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag), (.* 20[0-2][0-9])", datestring).group(2)
		
		if (place==""):
			place = "Zürich"
			
		newline = editiontype + '\t' + edition + '\t'  + datestring + '\t' + place + '\t8400\tRestaurant Huusmaa, Badenerstrasse 138, Zurich 8004' 

	
	if re.search("(Teilnehmer:|Anwesend waren:|Teilnehmer'':|Anwesend waren'':|Teilnehmende:|Teilnehmende'':)(.*)", line):
		attendees = re.search("(Teilnehmer:|Anwesend waren:|Teilnehmer'':|Anwesend waren'':|Teilnehmende:|Teilnehmende'':)(.*)", line).group(2)
		attendees = attendees.replace("•",",").replace("'", "")
		newline = newline + '\t' + attendees

	if not line.startswith("===") and not re.search("(Teilnehmer:|Anwesend waren:|Teilnehmer'':|Anwesend waren'':|Teilnehmende:|Teilnehmende'':)(.*)", line):
		protokoll = protokoll + line
		protokoll = protokoll.rstrip()
	
	
	edition = ""
	editiontype = ""
	place = ""
	attendees = ""
