# logic.py

def get_priority(severity):
    values = {
        "Critical": 1,
        "Severe": 2,
        "Moderate": 3,
        "Minor": 4
    }
    return values.get(severity, 5)


def get_priority_level(priority):
    values = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }
    return values.get(priority, 4)


def calculate_distance(location1, location2):
    distances = {
        ("Koramangala", "MG Road"): 3,
        ("Indiranagar", "MG Road"): 5,
        ("Whitefield", "MG Road"): 8,
        ("Koramangala", "Indiranagar"): 4,
        ("Indiranagar", "Whitefield"): 10
    }

    if location1 == location2:
        return 1

    if (location1, location2) in distances:
        return distances[(location1, location2)]

    if (location2, location1) in distances:
        return distances[(location2, location1)]

    return 10


def calculate_time(distance, traffic):
    if traffic == "Low":
        return distance + 4

    elif traffic == "Medium":
        return distance + 7

    elif traffic == "Heavy":
        return distance + 13

    return distance + 7


def is_suitable(ambulance, emergency):
    if ambulance["status"] != "Available":
        return False

    if ambulance["type"] != emergency["required_type"]:
        return False

    return True


def select_best_ambulance(ambulances, emergency):
    candidates = []

    for ambulance_id, ambulance in ambulances.items():

        if not is_suitable(ambulance, emergency):
            continue

        distance = calculate_distance(
            ambulance["location"],
            emergency["location"]
        )

        time = calculate_time(
            distance,
            emergency["traffic"]
        )

        candidates.append(
            (time, distance, ambulance_id)
        )

    if not candidates:
        return None

    candidates.sort()

    return candidates[0]


def get_zone_charge(distance):
    if distance <= 5:
        return 0
    elif distance <= 10:
        return 100
    elif distance <= 20:
        return 250
    else:
        return 500


def calculate_bill(distance, severity, traffic):
    base_charge = 500
    distance_charge = distance * 20

    if severity == "Critical":
        emergency_charge = 500
    else:
        emergency_charge = 300

    if traffic == "Heavy":
        traffic_charge = 200
    elif traffic == "Medium":
        traffic_charge = 100
    else:
        traffic_charge = 0

    zone_charge = get_zone_charge(distance)

    total = (
        base_charge
        + distance_charge
        + emergency_charge
        + traffic_charge
        + zone_charge
    )

    return total


def get_next_emergency(emergencies):
    waiting = []

    for emergency in emergencies:
        if emergency["status"] == "Waiting":
            waiting.append(emergency)

    if not waiting:
        return None

    waiting.sort(
        key=lambda e: (
            get_priority(e["severity"]),
            get_priority_level(e["priority"]),
            e["arrival"]
        )
    )

    return waiting[0]