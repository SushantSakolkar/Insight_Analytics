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



regEx = "(.*?) - - \[(.*?)\] \"(.*?)\" (.*?) (.*?)$"

def feature_2():
	start_time = time.time()
	# var section
	resCount = {}
	topTenResrc = {}
	minResCnt = 1
	minRes = ' '

	logFile = open ('./log_input/log.txt')
	for line in iter(logFile):

		logElements = re.match(regEx,line)

		# processing each line
		if logElements:


	###################################################### Feature 2 #############################################################

			if len(logElements.group(3).split(' '))>=2 :
				resource = logElements.group(3).split(' ')[1];
			
			
			# ignoring directory and login attempts in file count

			# Main ip vs count table modification
			if resCount.has_key(resource):
				try:
					resCount[resource]=resCount[resource] + float(logElements.group(5))/1024
				
				except:
					pass
			else :
				# insert new record in ip vs Count table
				try:
					resCount[resource]=float(logElements.group(5))/1024	
				except:
					resCount[resource]=0.0

			# Top 10 ip table modification
			if topTenResrc.has_key(resource):
				topTenResrc[resource]=resCount[resource]
				
				if minResCnt == resource :
					minRes = min(topTenResrc.items(), key=lambda x: x[1])[0]
					minResCnt = min(topTenResrc.items(), key=lambda x: x[1])[1]

			else :
				if len(topTenResrc)<10 :
					topTenResrc[resource]=resCount[resource]
					minRes = min(topTenResrc.items(), key=lambda x: x[1])[0]
					minResCount = min(topTenResrc.items(), key=lambda x: x[1])[1]
				else:
					# if ip qualifies to enter top 10
					if minResCount <= resCount[resource]:
						del topTenResrc[minRes]
						topTenResrc[resource]=resCount[resource]

						minRes = min(topTenResrc.items(), key=lambda x: x[1])[0]
						minCount = min(topTenResrc.items(), key=lambda x: x[1])[1]

	logFile.close()

	# Feature 2
		# Save old reference of stdout
	oldstdout = sys.stdout

	# Open file for Sys out
	sys.stdout = open('./log_output/resources.txt', 'w')
	sorted_dictionary = OrderedDict(sorted(topTenResrc.items(), key=lambda kv: kv[1], reverse=True))
	for key in sorted_dictionary :
		print str(key)

	# Restore old reference of stdout	
	sys.stdout = oldstdout
	print "\n Output Stored in resources.txt !! \n"
	print "---Feature 2 took %s seconds ---" % (time.time() - start_time)





