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
			if firstRecord == 0 and q.empty() :
				startTime = currentTimestamp
				heapCount = 1 
				timeWindow = currentTimestamp + timedelta(hours =1)
				startTT = logElements.group(2) # end to end complete timeStamp
				nextSecondString = logElements.group(2)
				ttCount = 1
				firstRecord = 1
			
			# It is not a first record.
			else :
				
				# If current timeStamp fits in 1 hour window, insert into queue
				
				if currentTimestamp <= timeWindow :
					if logElements.group(2) == startTT :
						ttCount = ttCount + 1
					else :

						q.put((startTT,ttCount))   # A queue of timestamp and its count
						qMemberCount = qMemberCount + ttCount

						
						startTT = logElements.group(2)
						ttCount = 1
						
				
				# current time is greater than 1 hour from last recorded slot-startTime
				else :

					q.put((startTT,ttCount))   # A queue of timestamp and its count
					qMemberCount = qMemberCount + ttCount				

					# loop till the timeslot such that, the slot and current time are within 1 hour window
					while not q.empty() and timeWindow < currentTimestamp :
						key = q.get()

						# initially filling heap with first 10 saved slots as (count, timeslot) object
						if heapCount < 11 :
							
							if (key [0] == nextSecondString) :
								heapq.heappush(topTenSlotHeap, (qMemberCount,key[0]))
								heapCount = heapCount + 1
								pushedTTString = key[0]
								pushedTTTime = datetime.strptime(key[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
								nextSecondTT = pushedTTTime + timedelta(seconds =1 )
								temp = str(nextSecondTT)
								nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"


							else :
								while nextSecondTT <= currentTimestamp :
									if heapCount < 11 :
										heapq.heappush(topTenSlotHeap, (qMemberCount,nextSecondString))
									else :
										if  topTenSlotHeap[0][0] < qMemberCount :
											heapq.heappushpop(topTenSlotHeap,(qMemberCount,nextSecondString))
									heapCount = heapCount + 1
									pushedString = nextSecondString
									pushedTTTime = datetime.strptime(pushedString.split(' ')[0], "%d/%b/%Y:%H:%M:%S")
									nextSecondTT = pushedTTTime + timedelta(seconds =1)
									temp = str(nextSecondTT)
									nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"


						# there are already 10 elements in heap we need to replace minimum
						else :
							# insert into heap only if slot count is greater than heap minimum	 
							if topTenSlotHeap[0][0] < qMemberCount :
								if (key [0] == nextSecondString) :
									heapq.heappushpop(topTenSlotHeap, (qMemberCount,key[0]))
									pushedTTString = key[0]
									pushedTTTime = datetime.strptime(key[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
									nextSecondTT = pushedTTTime + timedelta(seconds =1 )
									temp = str(nextSecondTT)
									nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"
 	
							else :
								while nextSecondTT <= currentTimestamp :
									heapq.heappushpop(topTenSlotHeap, (qMemberCount,nextSecondString))

									pushedString = nextSecondString
									pushedTTTime = datetime.strptime(pushedString.split(' ')[0], "%d/%b/%Y:%H:%M:%S")
									nextSecondTT = pushedTTTime + timedelta(seconds =1)
									temp = str(nextSecondTT)
									nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"

						qMemberCount = qMemberCount - int(key[1])

					# update queue start time as starting slot and set 1 hour window for next iteration
						if not q.empty() :
							startTime = datetime.strptime(q.queue[0][0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
							timeWindow = startTime + timedelta(hours =1 )
						else :
							startTime = datetime.strptime(logElements.group(2).split(' ')[0], "%d/%b/%Y:%H:%M:%S")

							timeWindow = startTime + timedelta(hours =1 )
					# since new slot is within the one hour range of 1st slot in  queue add it to queue

					startTT = logElements.group(2)
					ttCount = 1
								

	logFile.close()

	# inserting last series of duplicate timeslots or last timeslot
	q.put((startTT,ttCount))
	qMemberCount = qMemberCount + ttCount

	while not q.empty() :
		key = q.get()

		# initially filling heap with first 10 saved slots as (count, timeslot) object
		if heapCount < 11 :

			if (key [0] == nextSecondString) :
				heapq.heappush(topTenSlotHeap, (qMemberCount,key[0]))
				heapCount = heapCount + 1
				pushedTTString = key[0]
				pushedTTTime = datetime.strptime(key[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
				nextSecondTT = pushedTTTime + timedelta(seconds =1 )
				temp = str(nextSecondTT)
				nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400" 
			else :
				currentTimestamp = datetime.strptime(key[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")

				while nextSecondTT <= currentTimestamp :
					if heapCount < 11 :
						heapq.heappush(topTenSlotHeap, (qMemberCount,nextSecondString))
					else :
						if  topTenSlotHeap[0][0] < qMemberCount :
							heapq.heappushpop(topTenSlotHeap,(qMemberCount,nextSecondString))
					
					heapCount = heapCount + 1
					pushedString = nextSecondString
					pushedTTTime = datetime.strptime(pushedString.split(' ')[0], "%d/%b/%Y:%H:%M:%S")
					nextSecondTT = pushedTTTime + timedelta(seconds =1)
					temp = str(nextSecondTT)
					nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"

		# there are already 10 elements in heap we need to replace minimum
		else :
			# insert into heap only if slot count is greater than heap minimum	 
			if topTenSlotHeap[0][0] < qMemberCount :
				removedItem = heapq.heappushpop(topTenSlotHeap, (qMemberCount,key[0]))
				if (key [0] == nextSecondString) :
					heapq.heappushpop(topTenSlotHeap, (qMemberCount,key[0]))
					pushedTTString = key[0]
					pushedTTTime = datetime.strptime(key[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
					nextSecondTT = pushedTTTime + timedelta(seconds =1 )
					temp = str(nextSecondTT)
					nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1] + "/" +temp.split(' ')[0].split('-')[0]]+":"+temp.split(' ')[1]+ " -0400" 	
				else :
					while nextSecondTT <= currentTimestamp :
						heapq.heappushpop(topTenSlotHeap, (qMemberCount,nextSecondString))
						heapCount = heapCount + 1
						pushedString = nextSecondString
						pushedTTTime = datetime.strptime(pushedString.split(' ')[0], "%d/%b/%Y:%H:%M:%S")
						nextSecondTT = pushedTTTime + timedelta(seconds =1)
						temp = str(nextSecondTT)
						nextSecondString = temp.split(' ')[0].split('-')[2]+"/"+ months[temp.split(' ')[0].split('-')[1]] + "/" +temp.split(' ')[0].split('-')[0]+":"+temp.split(' ')[1]+ " -0400"


		qMemberCount = qMemberCount - int(key[1])

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
		print str(key)+","+ str(sorted_dictionary[key])

	# Restore old reference of stdout	
	sys.stdout = oldstdout
	print "\n--- Feature 3 took %s seconds --------" % (time.time() - start_time)
	print   "--- Output Stored in hours.txt !!--- \n"







	


