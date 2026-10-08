import heapq

# ============================================================
# AMBULANCE DISPATCH OPTIMIZATION SYSTEM
# Terminal-based Python application
# ============================================================

# -----------------------------
# CONFIGURED PROJECT DATA
# -----------------------------

# Distance values are project/demo values in kilometres.
# Add more location pairs here if your project needs them.
DISTANCES = {
    ("Koramangala", "MG Road"): 3.0,
    ("MG Road", "Koramangala"): 3.0,

    ("Indiranagar", "MG Road"): 5.0,
    ("MG Road", "Indiranagar"): 5.0,

    ("Whitefield", "MG Road"): 8.0,
    ("MG Road", "Whitefield"): 8.0,

    ("Jayanagar", "MG Road"): 6.0,
    ("MG Road", "Jayanagar"): 6.0,

    ("Koramangala", "Indiranagar"): 7.0,
    ("Indiranagar", "Koramangala"): 7.0,

    ("Koramangala", "Whitefield"): 14.0,
    ("Whitefield", "Koramangala"): 14.0,

    ("Indiranagar", "Whitefield"): 10.0,
    ("Whitefield", "Indiranagar"): 10.0,

    ("Jayanagar", "Koramangala"): 4.0,
    ("Koramangala", "Jayanagar"): 4.0,

    ("Jayanagar", "Indiranagar"): 9.0,
    ("Indiranagar", "Jayanagar"): 9.0,

    ("Jayanagar", "Whitefield"): 16.0,
    ("Whitefield", "Jayanagar"): 16.0,
}

VALID_LOCATIONS = {
    location
    for pair in DISTANCES.keys()
    for location in pair
}

# Billing constants
BASE_CHARGE = 500.0
RATE_PER_KM = 32.0

EMERGENCY_CHARGES = {
    "Critical": 500.0,
    "Severe": 350.0,
    "Moderate": 200.0,
    "Minor": 100.0,
}

TRAFFIC_CHARGES = {
    "Low": 200.0,
    "Normal": 250.0,
    "Medium": 300.0,
    "Heavy": 400.0,
}

# Minutes per kilometre.
# These values make the design-document example work:
# 5 km + Low traffic = 9 min
# 3 km + Heavy traffic ≈ 16 min
TRAFFIC_TIME_MULTIPLIER = {
    "Low": 1.8,
    "Normal": 2.5,
    "Medium": 3.5,
    "Heavy": 16 / 3,
}

VALID_STATUSES = {
    "Available",
    "Dispatched",
    "On the Way",
    "At Patient Location",
    "Transporting Patient",
    "At Hospital",
    "Returning",
    "Busy",
    "Unavailable",
}


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def normalize_choice(value: str, choices: list[str]) -> str | None:
    """Return the correctly capitalized choice or None."""
    cleaned = value.strip().lower()

    for choice in choices:
        if cleaned == choice.lower():
            return choice

    return None


def calculate_distance(from_location: str, to_location: str) -> float:
    """Return configured distance between two locations."""
    if from_location == to_location:
        return 0.0

    key = (from_location, to_location)

    if key not in DISTANCES:
        return -1.0

    return DISTANCES[key]


def estimate_response_time(distance: float, traffic: str) -> float:
    """Estimate response time using distance and traffic."""
    if distance < 0:
        return -1.0

    traffic = normalize_choice(
        traffic,
        ["Low", "Normal", "Medium", "Heavy"]
    )

    # Design document says use Normal if traffic information is unavailable.
    if traffic is None:
        traffic = "Normal"

    return round(distance * TRAFFIC_TIME_MULTIPLIER[traffic], 1)


def is_suitable(ambulance_type: str, required_type: str) -> bool:
    """
    Check ambulance suitability.

    Project assumption:
    Advanced ambulances can serve Advanced or Basic requests.
    Basic ambulances can serve only Basic requests.
    """
    ambulance_type = ambulance_type.strip().lower()
    required_type = required_type.strip().lower()

    if required_type == "basic":
        return ambulance_type in {"basic", "advanced"}

    if required_type == "advanced":
        return ambulance_type == "advanced"

    return False


def get_priority(severity: str, priority: str) -> int:
    """
    Convert severity + priority into one numeric score.
    Smaller number = higher urgency.
    """
    severity_rank = {
        "Critical": 1,
        "Severe": 2,
        "Moderate": 3,
        "Minor": 4,
    }

    priority_rank = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    severity_value = severity_rank.get(severity, 4)
    priority_value = priority_rank.get(priority, 3)

    # Severity is the main factor; stated priority breaks differences inside it.
    return severity_value * 10 + priority_value


def get_zone(distance: float) -> str:
    """Return zone based on distance."""
    if distance <= 5:
        return "A"
    elif distance <= 10:
        return "B"
    elif distance <= 20:
        return "C"
    return "D"


def calculate_bill(
    distance: float,
    emergency_level: str,
    traffic: str,
    zone: str
) -> float:
    """Calculate estimated ambulance bill."""
    if distance < 0:
        return 0.0

    zone_charge = {
        "A": 0.0,
        "B": 100.0,
        "C": 250.0,
        "D": 500.0,
    }

    emergency_charge = EMERGENCY_CHARGES.get(emergency_level, 0.0)
    traffic_charge = TRAFFIC_CHARGES.get(traffic, TRAFFIC_CHARGES["Normal"])
    distance_charge = distance * RATE_PER_KM

    total = (
        BASE_CHARGE
        + distance_charge
        + emergency_charge
        + traffic_charge
        + zone_charge.get(zone, 0.0)
    )

    return round(total, 2)


def refresh_hospital_counts(hospitals: dict, ambulances: dict) -> None:
    """Recalculate ambulance counts for every hospital."""
    for hospital in hospitals.values():
        hospital["total"] = 0
        hospital["available"] = 0
        hospital["busy"] = 0
        hospital["returning"] = 0
        hospital["at_hospital"] = 0

    for ambulance in ambulances.values():
        hospital_id = ambulance["hospital_id"]

        if hospital_id not in hospitals:
            continue

        hospital = hospitals[hospital_id]
        hospital["total"] += 1

        status = ambulance["status"]

        if status == "Available":
            hospital["available"] += 1
        elif status in {
            "Busy",
            "Dispatched",
            "On the Way",
            "At Patient Location",
            "Transporting Patient",
        }:
            hospital["busy"] += 1
        elif status == "Returning":
            hospital["returning"] += 1
        elif status == "At Hospital":
            hospital["at_hospital"] += 1


# -----------------------------
# REGISTRATION FUNCTIONS
# -----------------------------

def register_hospital(hospitals: dict) -> None:
    """Add hospital with ID, name, location and ambulance counts."""
    hospital_id = input("Enter hospital ID: ").strip().upper()

    if hospital_id in hospitals:
        print("Error: Hospital ID already exists.")
        return

    name = input("Enter hospital name: ").strip()
    location = input("Enter location: ").strip().title()

    if location not in VALID_LOCATIONS:
        print("Error: Invalid configured location.")
        print("Valid locations:", ", ".join(sorted(VALID_LOCATIONS)))
        return

    hospitals[hospital_id] = {
        "hospital_id": hospital_id,
        "name": name,
        "location": location,
        "total": 0,
        "available": 0,
        "busy": 0,
        "returning": 0,
        "at_hospital": 0,
    }

    print(f"Hospital registered: {hospital_id}")


def register_ambulance(ambulances: dict, hospitals: dict) -> None:
    """Register an ambulance."""
    ambulance_id = input("Enter ambulance ID: ").strip().upper()

    if ambulance_id in ambulances:
        print("Error: Ambulance ID already exists.")
        return

    hospital_id = input("Enter hospital ID: ").strip().upper()

    if hospital_id not in hospitals:
        print("Error: Hospital ID does not exist.")
        return

    location = input("Enter current location: ").strip().title()

    if location not in VALID_LOCATIONS:
        print("Error: Invalid configured location.")
        print("Valid locations:", ", ".join(sorted(VALID_LOCATIONS)))
        return

    ambulance_type = normalize_choice(
        input("Enter type (Basic/Advanced): "),
        ["Basic", "Advanced"]
    )

    if ambulance_type is None:
        print("Error: Invalid ambulance type.")
        return

    status_input = input(
        "Enter status (press Enter for Available): "
    ).strip()

    if status_input == "":
        status = "Available"
    else:
        status = normalize_choice(status_input, list(VALID_STATUSES))

    if status is None:
        print("Error: Invalid status.")
        return

    ambulances[ambulance_id] = {
        "ambulance_id": ambulance_id,
        "hospital_id": hospital_id,
        "type": ambulance_type,
        "location": location,
        "status": status,
        "current_emergency": None,
    }

    refresh_hospital_counts(hospitals, ambulances)
    print(f"Ambulance registered: {ambulance_id}")


# -----------------------------
# EMERGENCY FUNCTIONS
# -----------------------------

def add_emergency(
    emergencies: dict,
    priority_queue: list,
    arrival_counter: list
) -> None:
    """Create emergency and add it to priority queue."""
    emergency_id = input("Enter emergency ID: ").strip().upper()

    if emergency_id in emergencies:
        print("Error: Emergency ID already exists.")
        return

    patient_location = input("Enter patient location: ").strip().title()

    if patient_location not in VALID_LOCATIONS:
        print("Error: Invalid configured location.")
        print("Valid locations:", ", ".join(sorted(VALID_LOCATIONS)))
        return

    severity = normalize_choice(
        input("Enter severity (Critical/Severe/Moderate/Minor): "),
        ["Critical", "Severe", "Moderate", "Minor"]
    )

    if severity is None:
        print("Error: Invalid severity.")
        return

    priority = normalize_choice(
        input("Enter priority (High/Medium/Low): "),
        ["High", "Medium", "Low"]
    )

    if priority is None:
        print("Error: Invalid priority.")
        return

    required_type = normalize_choice(
        input("Enter required ambulance type (Basic/Advanced): "),
        ["Basic", "Advanced"]
    )

    if required_type is None:
        print("Error: Invalid ambulance type.")
        return

    traffic_input = input(
        "Enter traffic (Low/Normal/Medium/Heavy): "
    ).strip()

    traffic = normalize_choice(
        traffic_input,
        ["Low", "Normal", "Medium", "Heavy"]
    )

    if traffic is None:
        print("Traffic unavailable/invalid -> using Normal traffic.")
        traffic = "Normal"

    arrival_counter[0] += 1
    arrival_order = arrival_counter[0]

    emergency = {
        "emergency_id": emergency_id,
        "patient_location": patient_location,
        "severity": severity,
        "priority": priority,
        "required_type": required_type,
        "traffic": traffic,
        "status": "Waiting",
        "arrival_order": arrival_order,
        "selected_ambulance": None,
    }

    emergencies[emergency_id] = emergency

    priority_value = get_priority(severity, priority)

    # Tuple:
    # (priority score, arrival order, emergency ID)
    # This automatically gives FIFO ordering for equal priorities.
    heapq.heappush(
        priority_queue,
        (priority_value, arrival_order, emergency_id)
    )

    print(f"Emergency added: {emergency_id}")


def show_waiting_emergencies(
    emergencies: dict,
    priority_queue: list
) -> None:
    """Display waiting emergencies in priority order."""
    if not priority_queue:
        print("No waiting emergencies.")
        return

    print("\nWaiting Emergencies:")

    for priority_value, arrival_order, emergency_id in sorted(priority_queue):
        emergency = emergencies.get(emergency_id)

        if emergency and emergency["status"] == "Waiting":
            print(
                f"{emergency_id} - "
                f"{emergency['severity']} - "
                f"{emergency['priority']} - "
                f"Arrival {arrival_order}"
            )


# -----------------------------
# AMBULANCE SEARCH + SELECTION
# -----------------------------

def find_nearby_ambulances(
    ambulances: dict,
    location: str,
    radius: float
) -> list:
    """Return available ambulances inside the given radius."""
    nearby = []

    for ambulance_id, ambulance in ambulances.items():
        if ambulance["status"] != "Available":
            continue

        distance = calculate_distance(
            ambulance["location"],
            location
        )

        if 0 <= distance <= radius:
            nearby.append((ambulance_id, distance))

    return nearby


def select_ambulance(
    ambulances: dict,
    emergency: dict
) -> tuple[str | None, float | None, float | None]:
    """Select the best available and suitable ambulance."""
    candidates = []

    for ambulance_id, ambulance in ambulances.items():

        # FR6: only Available ambulances can be dispatched.
        if ambulance["status"] != "Available":
            continue

        if not is_suitable(
            ambulance["type"],
            emergency["required_type"]
        ):
            continue

        distance = calculate_distance(
            ambulance["location"],
            emergency["patient_location"]
        )

        if distance < 0:
            continue

        response_time = estimate_response_time(
            distance,
            emergency["traffic"]
        )

        # Tie-breaking:
        # 1. Lower response time
        # 2. Lower distance
        # 3. Advanced ambulance preferred when otherwise equal
        # 4. Ambulance ID
        type_rank = 0 if ambulance["type"] == "Advanced" else 1

        candidates.append(
            (
                response_time,
                distance,
                type_rank,
                ambulance_id
            )
        )

    if not candidates:
        return None, None, None

    candidates.sort()
    best = candidates[0]

    return best[3], best[1], best[0]


# -----------------------------
# DISPATCH + UPDATE FUNCTIONS
# -----------------------------

def save_history(
    history: list,
    emergency: dict,
    ambulance: dict,
    bill: float,
    distance: float,
    response_time: float
) -> None:
    """Store dispatch details in history."""
    history.append(
        {
            "emergency_id": emergency["emergency_id"],
            "ambulance_id": ambulance["ambulance_id"],
            "distance": distance,
            "traffic": emergency["traffic"],
            "response_time": response_time,
            "bill": bill,
            "status": emergency["status"],
        }
    )


def dispatch_ambulance(
    ambulances: dict,
    hospitals: dict,
    emergencies: dict,
    priority_queue: list,
    history: list
) -> None:
    """Process highest-priority emergency and dispatch best ambulance."""
    if not priority_queue:
        print("No waiting emergencies.")
        return

    # Look at highest-priority emergency without removing it yet.
    priority_value, arrival_order, emergency_id = priority_queue[0]

    emergency = emergencies[emergency_id]

    ambulance_id, distance, response_time = select_ambulance(
        ambulances,
        emergency
    )

    if ambulance_id is None:
        print(
            f"Alert: No suitable available ambulance for {emergency_id}."
        )
        print("Emergency remains in the priority queue.")
        return

    # Now remove the emergency because an ambulance was found.
    heapq.heappop(priority_queue)

    ambulance = ambulances[ambulance_id]

    zone = get_zone(distance)
    bill = calculate_bill(
        distance,
        emergency["severity"],
        emergency["traffic"],
        zone
    )

    old_status = ambulance["status"]

    ambulance["status"] = "On the Way"
    ambulance["current_emergency"] = emergency_id

    emergency["status"] = "Dispatched"
    emergency["selected_ambulance"] = ambulance_id

    refresh_hospital_counts(hospitals, ambulances)

    save_history(
        history,
        emergency,
        ambulance,
        bill,
        distance,
        response_time
    )

    nearby = find_nearby_ambulances(
        ambulances,
        emergency["patient_location"],
        10.0
    )

    print("\n========== DISPATCH REPORT ==========")
    print(f"Emergency ID: {emergency_id}")
    print(f"Severity: {emergency['severity']}")
    print(f"Priority: {emergency['priority']}")
    print(f"Patient Location: {emergency['patient_location']}")
    print(f"Nearby Available Ambulances: {len(nearby)}")
    print(f"Selected Ambulance: {ambulance_id}")
    print(f"Ambulance Type: {ambulance['type']}")
    print(f"Distance: {distance:.1f} km")
    print(f"Traffic: {emergency['traffic']}")
    print(f"Estimated Response Time: {response_time:.1f} min")
    print(f"Status: {old_status} -> {ambulance['status']}")
    print(f"Zone: {zone}")
    print(f"Estimated Bill: Rs. {bill:.2f}")
    print("=====================================")


def update_ambulance(
    ambulances: dict,
    hospitals: dict,
    ambulance_id: str,
    status: str,
    location: str
) -> None:
    """Update ambulance status and location."""
    ambulance_id = ambulance_id.strip().upper()

    if ambulance_id not in ambulances:
        print("Error: Invalid ambulance ID.")
        return

    if location not in VALID_LOCATIONS:
        print("Error: Invalid configured location.")
        return

    normalized_status = normalize_choice(status, list(VALID_STATUSES))

    if normalized_status is None:
        print("Error: Invalid status.")
        return

    old_location = ambulances[ambulance_id]["location"]
    old_status = ambulances[ambulance_id]["status"]

    ambulances[ambulance_id]["status"] = normalized_status
    ambulances[ambulance_id]["location"] = location

    if normalized_status in {"Available", "At Hospital"}:
        ambulances[ambulance_id]["current_emergency"] = None

    refresh_hospital_counts(hospitals, ambulances)

    print(f"Ambulance {ambulance_id}")
    print(f"Status: {old_status} -> {normalized_status}")
    print(f"Old location: {old_location}")
    print(f"New location: {location}")
    print("Location/status updated successfully.")


# -----------------------------
# DISPLAY FUNCTIONS
# -----------------------------

def show_hospitals(hospitals: dict) -> None:
    """Display hospital ambulance counts."""
    if not hospitals:
        print("No hospitals registered.")
        return

    print("\n========== HOSPITAL STATUS ==========")

    for hospital_id, hospital in hospitals.items():
        print(f"\nHospital {hospital_id}: {hospital['name']}")
        print(f"Location: {hospital['location']}")
        print(f"Total: {hospital['total']}")
        print(f"Available: {hospital['available']}")
        print(f"Busy/Dispatched: {hospital['busy']}")
        print(f"Returning: {hospital['returning']}")
        print(f"At Hospital: {hospital['at_hospital']}")

    print("=====================================")


def show_ambulances(ambulances: dict) -> None:
    """Display all ambulance records."""
    if not ambulances:
        print("No ambulances registered.")
        return

    print("\n========== AMBULANCES ==========")

    for ambulance_id, ambulance in ambulances.items():
        print(
            f"{ambulance_id} | "
            f"Hospital: {ambulance['hospital_id']} | "
            f"Type: {ambulance['type']} | "
            f"Location: {ambulance['location']} | "
            f"Status: {ambulance['status']} | "
            f"Emergency: {ambulance['current_emergency']}"
        )

    print("================================")


def show_history(history: list) -> None:
    """Display dispatch history."""
    if not history:
        print("No dispatch history.")
        return

    print("\n========== DISPATCH HISTORY ==========")

    for record in history:
        print(
            f"{record['emergency_id']} -> "
            f"{record['ambulance_id']} -> "
            f"{record['distance']:.1f} km -> "
            f"{record['traffic']} Traffic -> "
            f"{record['response_time']:.1f} min -> "
            f"Rs. {record['bill']:.2f} -> "
            f"{record['status']}"
        )

    print("======================================")


# -----------------------------
# OPTIONAL DEMO DATA
# -----------------------------

def load_demo_data(hospitals: dict, ambulances: dict) -> None:
    """Load simple sample data for quick testing."""
    if hospitals or ambulances:
        print("Demo data not loaded because records already exist.")
        return

    hospitals["H01"] = {
        "hospital_id": "H01",
        "name": "City Hospital",
        "location": "Indiranagar",
        "total": 0,
        "available": 0,
        "busy": 0,
        "returning": 0,
        "at_hospital": 0,
    }

    hospitals["H02"] = {
        "hospital_id": "H02",
        "name": "Metro Hospital",
        "location": "Whitefield",
        "total": 0,
        "available": 0,
        "busy": 0,
        "returning": 0,
        "at_hospital": 0,
    }

    ambulances["A01"] = {
        "ambulance_id": "A01",
        "hospital_id": "H01",
        "type": "Advanced",
        "location": "Koramangala",
        "status": "Available",
        "current_emergency": None,
    }

    ambulances["A02"] = {
        "ambulance_id": "A02",
        "hospital_id": "H01",
        "type": "Basic",
        "location": "Indiranagar",
        "status": "Busy",
        "current_emergency": "E999",
    }

    ambulances["A03"] = {
        "ambulance_id": "A03",
        "hospital_id": "H02",
        "type": "Advanced",
        "location": "Indiranagar",
        "status": "Available",
        "current_emergency": None,
    }

    ambulances["A04"] = {
        "ambulance_id": "A04",
        "hospital_id": "H02",
        "type": "Advanced",
        "location": "Whitefield",
        "status": "Returning",
        "current_emergency": None,
    }

    refresh_hospital_counts(hospitals, ambulances)
    print("Demo hospitals and ambulances loaded successfully.")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

def main() -> None:
    hospitals = {}
    ambulances = {}
    emergencies = {}

    # Priority queue stores:
    # (priority_value, arrival_order, emergency_id)
    priority_queue = []

    history = []

    # List used so add_emergency() can update the counter.
    arrival_counter = [0]

    while True:
        print("\n==========================================")
        print(" AMBULANCE DISPATCH OPTIMIZATION SYSTEM")
        print("==========================================")
        print("1. Register Hospital")
        print("2. Register Ambulance")
        print("3. Add Emergency")
        print("4. View Waiting Emergencies")
        print("5. Dispatch Next Emergency")
        print("6. View Hospital Status")
        print("7. View Ambulances")
        print("8. Update Ambulance Status/Location")
        print("9. View Dispatch History")
        print("10. Load Demo Data")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            register_hospital(hospitals)

        elif choice == "2":
            register_ambulance(ambulances, hospitals)

        elif choice == "3":
            add_emergency(
                emergencies,
                priority_queue,
                arrival_counter
            )

        elif choice == "4":
            show_waiting_emergencies(
                emergencies,
                priority_queue
            )

        elif choice == "5":
            dispatch_ambulance(
                ambulances,
                hospitals,
                emergencies,
                priority_queue,
                history
            )

        elif choice == "6":
            show_hospitals(hospitals)

        elif choice == "7":
            show_ambulances(ambulances)

        elif choice == "8":
            ambulance_id = input(
                "Enter ambulance ID: "
            ).strip().upper()

            status = input(
                "Enter new status: "
            ).strip()

            location = input(
                "Enter new location: "
            ).strip().title()

            update_ambulance(
                ambulances,
                hospitals,
                ambulance_id,
                status,
                location
            )

        elif choice == "9":
            show_history(history)

        elif choice == "10":
            load_demo_data(hospitals, ambulances)

        elif choice == "0":
            print("Program ended.")
            break

        else:
            print("Error: Invalid menu choice.")


if __name__ == "__main__":
    main()
