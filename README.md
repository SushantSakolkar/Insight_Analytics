# Project description can be found at :  
https://github.com/InsightDataScience/fansite-analytics-challenge  
--------------------------------------------------------------------------//

# Steps to Execute :-   
	Go to "fansite-analytics-challenge" directory  
	Execute command "./run.sh" :- "Caution :- This removes existing output files !!!"  
	Select option from 1 to 5 by entering the number  
	To exit press 6  
--------------------------------------------------------------------------//

# One additional feature added :-   
One can run all analytics sequenctially by selecting option 5.  
--------------------------------------------------------------------------//  

# Code Structure :-   
  
Run.sh calls process_log.py  
	process_log.py calls one of :  
		Feature_1.py  
		Feature_2.py  
		Feature_3.py  
		Feature_4.py  
		or All  
Pressing 6 Terminates the process !  
--------------------------------------------------------------------------//  

Algos summary :-
 
Feature_1.py :

	2 Data Structers :- 
		Dictionary of IP vs Count
		Dictionary of Top 10 IPs at any time.

	logic :- 
		Min count is maintained for top 10 IP Dictionary.
		The moment IP's count exceeds minimum,
			minIP is removed and current record is inserted.
			minIP and minCount calculated again.
		
----------------------------

Feature_2.py

	2 Data Structers :- 
		Dictionary of Resource vs Count
		Dictionary of Top 10 resources at any time.

	logic :- 
		Min count is maintained for top 10 resource Dictionary.
		The moment resource's count exceeds minimum,
			minResource is removed and current record is inserted.
			minResource and minCount calculated again.

Assumptions :- 
	Folder names such as "abc/" and "/login" are included as fileNames to match as per provided test case.
	"/" is also considered as file name

----------------------------		
	
Feature_3.py

	2 Data structures :-
		Queue(Timestamp,countOfTimeStamp)
		Heap which holds top 10 timestamps

	logic :-
		Keep adding timestamp and its repeataion count as object element of queue
		The moment Timestamp which is more than 1 hr from 1st timestamp arrives,
			Take cut of queue, push the (Sum of queue timestamps & timestamp) to heap of size 10.
			Add one second to previous timestamp and check for 1 hour window again.
			Repeat process until TimeWindow becomes less than 1 hour.
		Empty the queue for leftover record consideration by pushing in heap. 

Challenges faced :- 
	String to TimeStamp conversion, Timestamp to String conversion takes significant time. 

----------------------------

Feature_4.py

	2 Data Structures :-
		A dictionary for possible block ips ( ip , ( TT1, TT2 ) )
		A dictionary for blocked ips ( ip, last occurance TT)


	logic :-
		process request only if ip is not present in Blocked list or its been more than 5 minutes since it was blocked.
		Maintain 2 timestamp for ip, keep filling them if they are in 20 seconds window
		The moment 3rd denied request comes block the ip
		if 3rd request is successful login, remove ip from possible dict.
	
---------------------------------------------------------------------------------------------------------------------------------//
