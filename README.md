Ambulance Dispatch Optimization System
1. Project Overview

The Ambulance Dispatch Optimization System is a terminal-based Python application designed to manage emergency requests and efficiently assign the most suitable ambulance.

The system considers:

Emergency severity
Emergency priority
Ambulance availability
Ambulance type
Distance
Traffic conditions
Response time
Hospital availability

The system also calculates an estimated emergency bill and maintains dispatch history.

2. System Workflow

The overall workflow is:

Hospital Registration → Ambulance Registration → Emergency Request → Priority Queue → Ambulance Filtering → Distance & Traffic Check → Ambulance Selection → Dispatch → Billing → History

Workflow Steps
Register hospitals.
Register ambulances under hospitals.
Add emergency requests.
Store emergencies in a priority queue.
Process the highest-priority emergency.
Remove unavailable ambulances from consideration.
Check ambulance type suitability.
Find nearby ambulances.
Calculate distance.
Estimate response time using traffic.
Select the most suitable ambulance.
Dispatch the ambulance.
Update ambulance status and location.
Calculate the estimated bill.
Store dispatch details in history.

3. Key Features
Hospital Management:
Register hospitals.
Store hospital ID, name, and location.
Track ambulance availability.
Ambulance Management:
Register ambulances.
Store ambulance ID, hospital ID, type, location, and status.
Track available, dispatched, returning, and other statuses.
Emergency Management:
Add emergency requests.
Store patient location, severity, priority, required ambulance type, and traffic.
Maintain emergency arrival order.
Priority Queue:
Emergencies are processed according to priority.
Higher-priority emergencies are handled first.
If priority is the same, earlier emergencies are handled first using FIFO.
Ambulance Selection:
Only available ambulances are considered.
Busy, Returning, and Unavailable ambulances are excluded.
Ambulance type suitability is checked.
Distance and traffic are considered.
The most suitable ambulance is selected.
Billing:
Calculates estimated emergency charges.
Considers distance, emergency level, traffic, and zone.
Dispatch History
Stores completed dispatch information.
Includes ambulance, emergency, distance, response time, traffic, bill, and final status.

5. Data Structures

The project mainly uses Python dictionaries, lists, and a priority queue.

Data Structure	Usage
Dictionary	Hospitals, ambulances, emergencies
List	Dispatch history and collections
Priority Queue	Ordering emergency requests
Tuple	Priority queue entries
Emergency Queue

Emergency requests are organized using:

(priority, arrival_order, emergency_id)

This ensures that emergencies with the same priority are processed according to their arrival order.

5. System Components
Component	Information Stored
Hospital	Hospital ID, name, location, ambulance counts
Ambulance	ID, hospital, type, location, status
Emergency	ID, patient location, severity, priority, required type, traffic
Priority Queue	Priority, arrival order, emergency ID
History	Emergency, ambulance, distance, response time, bill

7. Emergency Priority

The system considers both severity and priority when processing emergencies.

Priority levels:

Priority	Level
1	Critical
2	Severe
3	Moderate
4	Minor

If two emergencies have the same priority:

Earlier arrival → Higher processing preference

If the arrival order is also the same, the emergency ID can be used as a final tie-breaker.

7. Ambulance Selection Logic

The system does not simply select the closest ambulance.

It follows multiple checks:

Step 1 — Availability

Only ambulances with an Available status are considered.

Step 2 — Type Suitability

The ambulance must be suitable for the emergency's required type.

Step 3 — Nearby Ambulances

The system checks ambulances within the configured radius.

Step 4 — Distance

The configured distance between the ambulance and patient location is calculated.

Step 5 — Traffic

Traffic conditions are considered while estimating response time.

Step 6 — Final Selection

The most suitable ambulance is selected based on:

Priority
Severity
Ambulance suitability
Distance
Traffic
Response time
8. Location & Distance

The project uses predefined/configured locations and distances.

It does not use a live Google Maps API.

The configured distance is used for:

Nearby ambulance checking
Response-time calculation
Ambulance comparison
Billing

So the system simulates location-based dispatch rather than using real-time GPS.

9. Traffic & Response Time

Traffic affects the estimated response time.

A farther ambulance can sometimes be selected if it has a better traffic condition and can reach the patient faster.

Example
Ambulance	Distance	Traffic	Response Time
A01	3 km	Heavy	16 min
A03	5 km	Low	9 min

Therefore, A03 can be selected even though it is farther away, because its estimated response time is lower.

10. Ambulance Status

The system supports ambulance statuses such as:

Available
Dispatched
On the Way
At Patient Location
Transporting Patient
At Hospital
Returning

When an ambulance is dispatched, its status and hospital availability count are updated.

11. Hospital Availability

The system tracks ambulance availability at hospitals.

It can maintain counts for:

Total ambulances
Available ambulances
Busy/dispatched ambulances
Returning ambulances
Ambulances currently at hospital

This helps determine whether another ambulance or hospital should be considered.

12. Billing System

The estimated bill follows:

Total = Base + Distance + Emergency + Traffic + Zone

Zone Charges
Zone	Distance	Charge
A	≤ 5 km	₹0
B	5–10 km	₹100
C	10–20 km	₹250
D	> 20 km	₹500
Example
Base = ₹500
Distance = ₹160
Emergency = ₹500
Traffic = ₹200
Zone = ₹100
Total

₹1460

13. Dispatch History

After an ambulance is dispatched, the system records:

Emergency ID
Ambulance ID
Distance
Traffic condition
Estimated response time
Estimated bill
Final status

This allows previous dispatches to be reviewed.

14. Main Functions
Function	Purpose
register_hospital()	Registers a hospital
register_ambulance()	Registers an ambulance
add_emergency()	Adds an emergency request
get_priority()	Determines emergency priority
find_nearby_ambulances()	Finds nearby ambulances
calculate_distance()	Calculates/configures distance
estimate_response_time()	Estimates response time
is_suitable()	Checks ambulance suitability
select_ambulance()	Selects the best ambulance
dispatch_ambulance()	Dispatches an ambulance
update_ambulance()	Updates status and location
calculate_bill()	Calculates estimated bill
save_history()	Saves dispatch history
main()	Runs the complete application
15. Project Structure
Ambulance-Dispatch-Optimization/
│
├── main.py
├── test_ambulance.py
└── README.md
main.py

Contains the main application, menu, ambulance management, emergency processing, selection, billing, and dispatch logic.

test_ambulance.py

Contains automated test cases for the system.

README.md

Contains project documentation.

16. Testing

The project contains 17 test cases covering the main functionality.

Test Case	Description
TC01	Register hospital
TC02	Register ambulance
TC03	Add emergency request
TC04	Process multiple emergencies
TC05	Same-priority FIFO
TC06	Busy ambulance exclusion
TC07	Nearby ambulance checking
TC08	Traffic response time
TC09	Ambulance type suitability
TC10	Best ambulance selection
TC11	Bill calculation
TC12	Status and location update
TC13	Dispatch history
TC14	No available ambulance
TC15	Invalid ID
TC16	Negative distance
TC17	Integrated workflow
Run Tests
pytest test_ambulance.py 

17. Edge Cases Handled

The system handles situations such as:

No available ambulance
No suitable ambulance nearby
Busy ambulance
Same emergency priority
Same distance
Same response time
Hospital with zero available ambulances
Invalid ambulance ID
Invalid hospital ID
Invalid location
Negative numeric values
Missing traffic information

If traffic information is missing, the system can use Normal traffic.

18. Technology Used
Python
Dictionaries
Lists
Priority Queue
Functions
Pytest
Terminal / CLI
19. How to Run
Run the application
python main.py
Run the tests
pytest test_ambulance.py

21. Limitations
The system is terminal-based.
Locations are predefined/configured.
It does not use live GPS.
It does not use Google Maps.
Traffic is configured/input rather than obtained from a live traffic API.
Billing is an estimated calculation based on configured rules.

23. Future Improvements

Possible future improvements include:

Live GPS integration
Google Maps/API integration
Real-time traffic data
Real-time ambulance tracking
Database integration
Web-based interface
Mobile application
Automatic notifications
Real-time hospital availability
22. Conclusion

The Ambulance Dispatch Optimization System provides a structured way to manage emergency requests and ambulance resources.

It combines priority queues, ambulance availability, type suitability, distance, traffic, response time, billing, and dispatch history to make ambulance allocation more efficient.

The system demonstrates how Python data structures and algorithms can be applied to a real-world emergency dispatch problem.
