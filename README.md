Ambulance Dispatch Optimization System:

The Ambulance Dispatch Optimization System is a menu-driven, terminal-based Python application designed to manage emergency requests and assign suitable ambulances. It prioritizes emergencies, checks ambulance availability and suitability, estimates response time based on distance and traffic, calculates estimated bills, and maintains dispatch history.

The system helps manage hospitals, ambulances, and emergency requests through a numbered menu. It uses dictionaries to store records, a priority queue to process emergencies, and functions to handle dispatch calculations and validation.

Features:
Hospital Management: Register hospitals, store their locations, and track ambulance counts and availability.
Ambulance Management: Register ambulances with unique IDs, hospital assignments, ambulance types, current locations, and statuses.
Emergency Registration: Create emergency requests with patient location, severity, priority, required ambulance type, and traffic conditions.
Priority Queue: Process emergencies according to severity and priority, using arrival order to break ties.
Ambulance Selection: Select a suitable available ambulance based on ambulance type, distance, and estimated response time.
Distance Calculation: Calculate distances between configured locations using predefined distance values.
Traffic-Based Response Time: Estimate ambulance response time using distance and traffic conditions.
Ambulance Status Updates: Update ambulance locations and statuses as their availability changes.
Billing System: Calculate estimated bills using base charges, distance charges, emergency severity, traffic, and distance zone.
Hospital Status: View total, available, busy, returning, and at-hospital ambulance counts.
Dispatch History: Record completed dispatch assignments, including the selected ambulance, distance, response time, and estimated bill.
Demo Data: Load predefined hospitals and ambulances to demonstrate the system.
Input Validation: Handle duplicate IDs, invalid locations, invalid ambulance types, invalid statuses, and other invalid inputs.
Edge-Case Handling: Keep emergencies waiting when no suitable ambulance is available and handle equal-priority emergencies using arrival order.

Requirements:
Python 3.10 or newer.
pytest for running unit tests.
A terminal or command-line interface.
No external database is required unless a database integration is added separately.

Setup:
Clone or download the project repository and open the project directory in your terminal.
Install pytest:
python -m pip install pytest

Run:
Run the application from the project directory:
python main.py
The program displays a numbered menu through which users can register hospitals, register ambulances, add emergencies, view waiting emergencies, dispatch ambulances, update ambulance details, and view dispatch history.
If demo data is available, it can be loaded to test the application without manually registering every record.

Run Tests:
Run the unit tests using:
python -m pytest -q
The tests check individual functions and important system behaviours, including registration, emergency prioritization, ambulance suitability, distance and response-time calculations, billing, status updates, dispatch history, and edge cases.

Using It:
The application is controlled through numbered terminal menus.
The main menu includes the following operations:
Register Hospital
Register Ambulance
Add Emergency
View Waiting Emergencies
Dispatch Next Emergency
View Hospital Status
View Ambulances
Update Ambulance Status/Location
View Dispatch History
Load Demo Data
Exit

 Features:
* **Hospital Management:** Register hospitals and track ambulance availability at each hospital.
* **Ambulance Management:** Register ambulances, assign them to hospitals, and update their locations and statuses.
* **Emergency Registration:** Record emergency IDs, patient locations, severity, priority, required ambulance type, and traffic conditions.
* **Emergency Prioritization:** Use a priority queue to process urgent emergencies first, with arrival order breaking ties.
* **Ambulance Selection:** Select a suitable available ambulance based on type, distance, and estimated response time.
* **Distance Calculation:** Calculate distances between predefined locations.
* **Traffic-Based Response Time:** Estimate response time using distance and traffic conditions.
* **Ambulance Status Tracking:** Track available, busy, returning, and other ambulance statuses.
* **Hospital Status:** Display total and available ambulances, along with their current statuses.
* **Billing System:** Calculate estimated bills using base, distance, emergency, traffic, and zone charges.
* **Dispatch History:** Store and display records of ambulance dispatches, including distance, response time, and estimated bill.
* **Demo Data:** Load predefined hospitals and ambulances for testing and demonstration.
* **Input Validation:** Handle duplicate IDs, invalid locations, invalid ambulance types, and invalid statuses.
* **Edge-Case Handling:** Handle situations such as no suitable ambulance being available, equal-priority emergencies, and invalid distance values.
* **Unit Testing:** Test core functions and important workflows to verify that the system behaves as expected.

  Example Workflow
Choice: 10

Demo data loaded.

Choice: 3

Enter emergency ID: E001
Enter patient location: MG Road
Enter severity: Critical
Enter priority: High
Enter required ambulance type: Advanced
Enter traffic: Low

Emergency E001 added to the waiting queue.

Choice: 4

Waiting emergencies displayed.

Choice: 5

========== DISPATCH REPORT ==========
Emergency ID: E001
Severity: Critical
Priority: High
Patient Location: MG Road
Selected Ambulance: A01
Distance: [calculated distance]
Estimated Response Time: [calculated time]
Estimated Bill: [calculated bill]
=====================================

Things worth knowing:
Emergencies are processed according to severity, priority, and arrival order.
Only available ambulances that satisfy the emergency's requirements are eligible for dispatch.
The closest ambulance is not necessarily the best choice because traffic affects estimated response time.
If no suitable ambulance is available, the emergency remains in the waiting queue.
Ambulance status and hospital counts are updated after dispatch.
Invalid traffic input defaults to Normal traffic in the current implementation.
Distances are based on configured location pairs rather than live map data.
The estimated bill is calculated using the project's predefined billing rules.

Project Structure:
.
├── main.py             Menu, user input, output and workflow
├── logic.py            Core calculations and dispatch logic
├── functions.py        Supporting application functions, if retained
├── test_cases.py       Unit tests
├── PRD.md              Product Requirements Document
├── Design_Document.md  System design and algorithms
└── README.md           Project overview and instructions

How It Is Built
main.py connects the application workflow to the terminal menu. It accepts user input, displays results, and invokes the relevant functions.
logic.py contains the core calculations and decision-making logic, such as distance calculation, response-time estimation, ambulance suitability, ambulance selection, priority calculation, zone determination, and bill calculation.
functions.py, if retained, contains supporting application functions. Its responsibilities should be clearly separated from the pure logic module.
test_cases.py contains tests that verify the behaviour of individual functions and important workflows.

The project uses dictionaries to organise hospital, ambulance, and emergency records by their IDs. A priority queue implemented with Python's heapq module helps process the most urgent emergency first.

Pure logic functions are designed to return results without directly handling terminal input or output. This separation makes the core calculations easier to test and maintain.

Data Structures:
Data Structure	Purpose
Dictionaries:	Store hospitals, ambulances, and emergency records using unique IDs.
Priority Queue:	Process emergencies according to their priority and arrival order.
Lists:	Maintain queue entries, arrival counters, and dispatch history.
Tuples:	Represent configured location pairs and associated distance lookups.

Dispatch and Billing
Ambulance Selection

The system evaluates eligible ambulances using their availability, type suitability, distance from the patient, and estimated response time.

Emergency Priority

Emergencies are ranked primarily by severity, with the stated priority used to distinguish urgency. Arrival order breaks ties when the priority values are equal.

Estimated Bill

The bill is calculated using the following components:

Total Bill =
    Base Charge
    + Distance Charge
    + Emergency Charge
    + Traffic Charge
    + Zone Charge

The application uses predefined charges and distance zones. The result is an estimated bill rather than a live quotation.

Testing:
Unit tests help verify that the system behaves as expected.
The test suite covers areas such as:
Hospital and ambulance registration.
Emergency creation and priority ordering.
FIFO handling for equal-priority emergencies.
Ambulance availability and suitability.
Distance and traffic-based response-time calculations.
Ambulance selection.
Bill calculation.
Ambulance status and location updates.
Dispatch history.
No suitable ambulance available.
Invalid IDs and negative distance.
Complete dispatch workflows.

Scope and Limitations:
The application is terminal-based and does not provide a graphical user interface.
Locations and distances are configured in advance; the system does not use live maps, GPS, or real-time traffic data.
Response times are estimates based on predefined distance and traffic rules.
Billing uses predefined charges and is not connected to a real payment system.
The system manages emergency requests and ambulance assignments using in-memory data structures unless persistent storage is implemented separately.
Data stored only in memory will not automatically remain available after the program exits.
The application is intended as an academic project and is not a replacement for a real emergency dispatch service.

Future Improvements:
Integrate live maps, GPS locations, and traffic information.
Add database storage for hospitals, ambulances, emergencies, and dispatch history.
Introduce a graphical user interface.
Add more advanced dispatch optimisation and route planning.
Implement user authentication and role-based access.
Add persistent emergency records and reporting.
Improve validation and expand automated test coverage.

Authors:

1. Madiha Shaik .S
2. Sanika raj
3. Gokul Reddy

Course: Program Design and Development

Institution: Atria University

Year: Second Year — Digital Transformation
