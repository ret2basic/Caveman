#!/usr/bin/env python3

import os
from os import listdir

def get_files():

	files = os.listdir("/root/crashes/")

	return files

def triage_files(files):

	for x in files:

		original_output = os.popen("exifsan " + x + " -verbose 2>&1").read()
		output = original_output
		
		# Getting crash reason
		crash = ''
		if "SEGV" in output:
			crash = "SEGV"
		elif "heap-buffer-overflow" in output:
			crash = "HBO"
		else:
			crash = "UNKNOWN"
		

		if crash == "HBO":
			output = output.split("\n")
			counter = 0
			while counter < len(output):
				if output[counter] == "=================================================================":
					target_line = output[counter + 1]
					target_line2 = output[counter + 2]
					counter += 1
				else:
					counter += 1
			target_line = target_line.split(" ")
			address = target_line[5].replace("0x","")
			

			target_line2 = target_line2.split(" ")
			operation = target_line2[0]
			

		elif crash == "SEGV":
			output = output.split("\n")
			counter = 0
			while counter < len(output):
				if output[counter] == "=================================================================":
					target_line = output[counter + 1]
					target_line2 = output[counter + 2]
					counter += 1
				else:
					counter += 1
			if "unknown address" in target_line:
				address = "00000000"
			else:
				address = None

			if "READ" in target_line2:
				operation = "READ"
			elif "WRITE" in target_line2:
				operation = "WRITE"
			else:
				operation = None

		log_name = (x.replace(".jpg","") + "." + crash + "." + address + "." + operation)
		f = open(log_name,"w+")
		f.write(original_output)
		f.close()


files = get_files()
triage_files(files)