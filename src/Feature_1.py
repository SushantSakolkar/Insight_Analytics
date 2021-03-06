import os.path
import datetime
import re
import time
import Queue
import heapq
from datetime import datetime, timedelta
from collections import defaultdict
from collections import OrderedDict
import sys

start_time = time.time()

regEx = "(.*?) - - \[(.*?)\] \"(.*?)\" (.*?) (.*?)$"

def feature_1():
	start_time = time.time()
	# var section
	ipCount = {}
	topTenIp = {}
	minCount = 1
	minIp = ' '

	try:
		logFile = open ('./log_input/log.txt')
	except IOError:
		print('!!! ..................  There was an error opening the file! .................... !!!')
		return

	for line in iter(logFile):

		logElements = re.match(regEx,line)

		# processing each line
		if logElements:
	###################################################### Feature 1 #############################################################

			# Main ip vs count table modification
			if ipCount.has_key(logElements.group(1)):
				ipCount[logElements.group(1)]=ipCount[logElements.group(1)] + 1

			else :
				# insert new record in ip vs Count table
				ipCount[logElements.group(1)]=1	
				
				
			# Top 10 ip table modification
			if topTenIp.has_key(logElements.group(1)):
				topTenIp[logElements.group(1)]=ipCount[logElements.group(1)]
				
				if minIp == logElements.group(1) :
					minIp = min(topTenIp.items(), key=lambda x: x[1])[0]
					minCount = min(topTenIp.items(), key=lambda x: x[1])[1]


			else :
				if len(topTenIp)<10 :
					topTenIp[logElements.group(1)]=ipCount[logElements.group(1)]
					minIp = min(topTenIp.items(), key=lambda x: x[1])[0]
					minCount = min(topTenIp.items(), key=lambda x: x[1])[1]

				else:
					# if ip qualifies to enter top 10
					if minCount <= ipCount[logElements.group(1)]:
						del topTenIp[minIp]
						topTenIp[logElements.group(1)]=ipCount[logElements.group(1)]

						minIp = min(topTenIp.items(), key=lambda x: x[1])[0]
						minCount = min(topTenIp.items(), key=lambda x: x[1])[1]


	logFile.close()

	# Save old reference of stdout
	oldstdout = sys.stdout

	# Open file for Sys out
	sys.stdout = open('./log_output/hosts.txt', 'w')

	sorted_dictionary = OrderedDict(sorted(topTenIp.items(), key=lambda kv: kv[1], reverse=True))
	for key in sorted_dictionary :
		print str(key)+","+ str(sorted_dictionary[key])


	# Restore old reference of stdout	
	sys.stdout = oldstdout
	print "\n---Output Stored in hosts.txt !!---"
	print "---Feature 1 took %s seconds --------" % (time.time() - start_time)





