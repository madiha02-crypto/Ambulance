# functions.py

from logic import (
    get_next_emergency,
    select_best_ambulance,
    calculate_distance,
    calculate_bill
)

hospitals = {}
ambulances = {}
emergencies = []
dispatch_history = []

arrival_order = 0


def register_hospital():
    hospital_id = input("Enter hospital ID: ")
    name = input("Enter hospital name: ")
    location = input("Enter hospital location: ")

    hospitals[hospital_id] = {
        "name": name,
        "location": location,
        "total": 0,
        "available": 0,
        "busy": 0,
        "returning": 0
    }

    print("Hospital registered.")


def register_ambulance():
    ambulance_id = input("Enter ambulance ID: ")
    hospital_id = input("Enter hospital ID: ")
    location = input("Enter ambulance location: ")
    ambulance_type = input("Enter ambulance type: ")

    if hospital_id not in hospitals:
        print("Hospital not found.")
        return

    ambulances[ambulance_id] = {
        "hospital": hospital_id,
        "location": location,
        "type": ambulance_type,
        "status": "Available"
    }

    hospitals[hospital_id]["total"] += 1
    hospitals[hospital_id]["available"] += 1

    print("Ambulance registered.")


def add_emergency():
    global arrival_order

    emergency_id = input("Enter emergency ID: ")
    location = input("Enter patient location: ")
    severity = input("Enter severity: ")
    priority = input("Enter priority: ")
    ambulance_type = input("Enter required ambulance type: ")
    traffic = input("Enter traffic: ")

    arrival_order += 1

    emergency = {
        "id": emergency_id,
        "location": location,
        "severity": severity,
        "priority": priority,
        "required_type": ambulance_type,
        "traffic": traffic,
        "arrival": arrival_order,
        "status": "Waiting"
    }

    emergencies.append(emergency)

    print("Emergency added.")


def show_next_emergency():
    emergency = get_next_emergency(emergencies)

    if emergency is None:
        print("No waiting emergency.")
        return

    print("\nNext Emergency")
    print("ID:", emergency["id"])
    print("Severity:", emergency["severity"])
    print("Priority:", emergency["priority"])
    print("Location:", emergency["location"])


def find_nearby_ambulances():
    emergency = get_next_emergency(emergencies)

    if emergency is None:
        print("No waiting emergency.")
        return

    print("\nNearby Ambulances")

    count = 0

    for ambulance_id, ambulance in ambulances.items():

        if ambulance["status"] != "Available":
            continue

        if ambulance["type"] != emergency["required_type"]:
            continue

        distance = calculate_distance(
            ambulance["location"],
            emergency["location"]
        )

        if distance <= 10:
            count += 1
            print(ambulance_id, "-", distance, "km")

    print("Nearby count:", count)


def dispatch_ambulance():
    emergency = get_next_emergency(emergencies)

    if emergency is None:
        print("No waiting emergency.")
        return

    result = select_best_ambulance(
        ambulances,
        emergency
    )

    if result is None:
        print("No suitable ambulance available.")
        return

    time, distance, ambulance_id = result

    ambulance = ambulances[ambulance_id]
    hospital = hospitals[ambulance["hospital"]]

    ambulance["status"] = "Dispatched"

    emergency["status"] = "Dispatched"

    hospital["available"] -= 1
    hospital["busy"] += 1

    dispatch_history.append({
        "emergency": emergency["id"],
        "ambulance": ambulance_id,
        "distance": distance,
        "time": time
    })

    print("\nAmbulance dispatched")
    print("Ambulance:", ambulance_id)
    print("Distance:", distance, "km")
    print("Time:", time, "minutes")


def update_status():
    ambulance_id = input("Enter ambulance ID: ")

    if ambulance_id not in ambulances:
        print("Ambulance not found.")
        return

    new_status = input("Enter new status: ")

    ambulance = ambulances[ambulance_id]
    ambulance["status"] = new_status

    print("Status updated.")


def update_location():
    ambulance_id = input("Enter ambulance ID: ")

    if ambulance_id not in ambulances:
        print("Ambulance not found.")
        return

    location = input("Enter new location: ")

    ambulances[ambulance_id]["location"] = location

    print("Location updated.")


def calculate_ambulance_bill():
    emergency_id = input("Enter emergency ID: ")

    record = None

    for item in dispatch_history:
        if item["emergency"] == emergency_id:
            record = item
            break

    if record is None:
        print("Dispatch not found.")
        return

    emergency = None

    for item in emergencies:
        if item["id"] == emergency_id:
            emergency = item
            break

    bill = calculate_bill(
        record["distance"],
        emergency["severity"],
        emergency["traffic"]
    )

    print("Total Bill:", bill)


def show_history():
    if not dispatch_history:
        print("No dispatch history.")
        return

    print("\nDispatch History")

    for item in dispatch_history:
        print(
            item["emergency"],
            "->",
            item["ambulance"],
            "|",
            item["distance"],
            "km"
        )