#!/usr/bin/python
import os.path
import dateutil.parser
import datetime
import re
import time
import Queue
import heapq
from datetime import datetime, timedelta
from collections import defaultdict
from collections import OrderedDict
import sys

from Feature_1 import feature_1
from Feature_2 import feature_2
from Feature_3 import feature_3
from Feature_4 import feature_4

#start_time = time.time()

regEx = "(.*?) - - \[(.*?)\] \"(.*?)\" (.*?) (.*?)$"

def run_analytics() :
	print "\n \n Available analytics are as follows :"
	print "====================================="
	print "1. Top 10 IPs"
	print "2. Top 10 Resources"
	print "3. Top 10 TimeSlots"
	print "4. Blocked Requests"
	print "5. All of the above"
	print "====================================="
	print " -------- To EXIT enter 6 -----------"

	choice = input("\n \nEnter number 1 to 6 for above choices : ")

	if choice == 1 :
		feature_1()
		run_analytics()

	elif choice == 2 :
		feature_2()
		run_analytics()

	elif choice == 3 :
		feature_3()
		run_analytics()

	elif choice == 4 :
		feature_4()
		run_analytics()

	elif choice == 5 :
		feature_1()
		feature_2()
		feature_3()
		feature_4()
		print "\n\n .......... All analytics performed. Exiting........ \n \n"

	elif choice == 6 :
		print "Exiting ........."

	else :
		choice= input("Bad Choice, please select a number between 1 to 6 : ")

run_analytics()
