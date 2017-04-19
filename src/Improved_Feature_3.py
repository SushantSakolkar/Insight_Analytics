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

start_time = time.time()

regEx = "(.*?) - - \[(.*?)\] \"(.*?)\" (.*?) (.*?)$"

months = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", 12:"Dec"}

def feature_3():
	start_time = time.time()
	# var section
	q = Queue.Queue()      #Queue for a Tiemslot instance
	timeSlotCount = {}     #Count of requests in a timeslot
	topTenSlotHeap = []    #Heap for top ten timeslots
	heapCount = 0
	qMemberCount = 0
	firstRecord = 0
	startTime =' '
	startTT = ' '
	ttCount = 0
	timeWindow = ' '

	logFile = open ('./log_input/log.txt')
	for line in iter(logFile):

		logElements = re.match(regEx,line)

		# processing each line
		if logElements:
		
	###################################################### Feature 3 #############################################################
			
			# converting Strig to timestamp for current record
			#currentTimestamp = dateutil.parser.parse(logElements.group(2).replace(':', ' ', 1))
			currentTimestamp = datetime.strptime(logElements.group(2).split(' ')[0], "%d/%b/%Y:%H:%M:%S")	

			# First record in Queue and first 1 hour window.
			if firstRecord == 0 :
				startTime = currentTimestamp
				qStart = startTime
				heapCount = 0 
				timeWindow = currentTimestamp + timedelta(hours =1)
				ttCount = 1
				firstRecord = 1
			
			# It is not a first record.
			else :
				
				# If current timeStamp fits in 1 hour window, insert into queue
				if currentTimestamp <= timeWindow :

					# if its a repeating record
					if currentTimestamp == startTime :
						ttCount = ttCount + 1

					# its a new record insert previous record with its count in queue.
					else :

						q.put((startTime,ttCount))   # A queue of timestamp and its count
						qMemberCount = qMemberCount + ttCount
						
						startTime = currentTimestamp
						ttCount = 1						
				
				# current time is greater than 1 hour from last recorded slot-startTime
				else :
					

					q.put((startTime,ttCount))   # A queue of timestamp and its count
					qMemberCount = qMemberCount + ttCount				
					
					# loop till the timeslot such that, the slot and current time are within 1 hour window
					while timeWindow < currentTimestamp :


						if heapCount < 10 :
							heapq.heappush(topTenSlotHeap, (qMemberCount,qStart))
							heapCount = heapCount + 1

						else :
							if topTenSlotHeap[0][0] < qMemberCount :
								heapq.heappushpop(topTenSlotHeap, (qMemberCount,qStart))

						if not q.empty() :
							if q.queue[0][0] == qStart :
								key = q.get()
								qMemberCount = qMemberCount- int(key[1])
						
						qStart = qStart + timedelta(seconds =1)
						timeWindow = qStart + timedelta(hours =1)						

					startTime = currentTimestamp
					ttCount = 1
					# since new slot is within the one hour range of 1st slot in  queue add it to queue
						

	logFile.close()

	# inserting last series of duplicate timeslots or last timeslot
	q.put((startTime,ttCount))
	qMemberCount = qMemberCount + ttCount

	
	topTenSlotDict = {}
	while topTenSlotHeap :
		element = heapq.heappop(topTenSlotHeap)
		topTenSlotDict[element[1]]=element[0]

	# Save old reference of stdout
	oldstdout = sys.stdout

	# Open file for Sys out
	sys.stdout = open('./log_output/hours.txt', 'w')

	# generating output file
	sorted_dictionary = OrderedDict(sorted(topTenSlotDict.items(), key=lambda (k, v): (-v, k)))
	for key in sorted_dictionary :
		print str(key).split(' ')[0].split('-')[2]+"/"+ months[ str(key).split(' ')[0].split('-')[1]] + "/" + str(key).split(' ')[0].split('-')[0]+":"+ str(key).split(' ')[1]+ " -0400"+","+ str(sorted_dictionary[key])

	# Restore old reference of stdout	
	sys.stdout = oldstdout
	print "\n--- Feature 3 took %s seconds --------" % (time.time() - start_time)
	print   "--- Output Stored in hours.txt !!--- \n"


