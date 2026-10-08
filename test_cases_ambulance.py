import pytest
import Main


# ============================================================
# TC01 - Register Hospital
# FR1
# ============================================================

def test_TC01_register_hospital(monkeypatch):
    hospitals = {}

    inputs = iter([
        "H01",
        "City Hospital",
        "MG Road"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    Main.register_hospital(hospitals)

    assert "H01" in hospitals
    assert hospitals["H01"]["name"] == "City Hospital"
    assert hospitals["H01"]["location"] == "MG Road"


# ============================================================
# TC02 - Register Ambulance
# FR2
# ============================================================

def test_TC02_register_ambulance(monkeypatch):
    hospitals = {
        "H01": {
            "hospital_id": "H01",
            "name": "City Hospital",
            "location": "MG Road",
            "total": 0,
            "available": 0,
            "busy": 0,
            "returning": 0,
            "at_hospital": 0
        }
    }

    ambulances = {}

    inputs = iter([
        "A01",
        "H01",
        "Koramangala",
        "Advanced",
        "Available"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    Main.register_ambulance(ambulances, hospitals)

    assert "A01" in ambulances
    assert ambulances["A01"]["hospital_id"] == "H01"
    assert ambulances["A01"]["type"] == "Advanced"
    assert ambulances["A01"]["status"] == "Available"


# ============================================================
# TC03 - Add Emergency Request
# FR3
# ============================================================

def test_TC03_add_emergency(monkeypatch):
    emergencies = {}
    priority_queue = []
    arrival_counter = [0]

    inputs = iter([
        "E001",
        "MG Road",
        "Critical",
        "High",
        "Advanced",
        "Low"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    Main.add_emergency(
        emergencies,
        priority_queue,
        arrival_counter
    )

    assert "E001" in emergencies
    assert emergencies["E001"]["status"] == "Waiting"
    assert len(priority_queue) == 1


# ============================================================
# TC04 - Process Multiple Emergencies
# FR4
# ============================================================

def test_TC04_highest_priority_processed_first():
    hospitals = {}
    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        }
    }

    emergencies = {
        "E001": {
            "emergency_id": "E001",
            "patient_location": "MG Road",
            "severity": "Moderate",
            "priority": "Low",
            "required_type": "Advanced",
            "traffic": "Normal",
            "status": "Waiting",
            "arrival_order": 1,
            "selected_ambulance": None
        },
        "E002": {
            "emergency_id": "E002",
            "patient_location": "MG Road",
            "severity": "Critical",
            "priority": "High",
            "required_type": "Advanced",
            "traffic": "Normal",
            "status": "Waiting",
            "arrival_order": 2,
            "selected_ambulance": None
        }
    }

    # Heap order: E002 has higher priority than E001.
    priority_queue = [
        (11, 2, "E002"),
        (33, 1, "E001")
    ]

    history = []

    Main.dispatch_ambulance(
        ambulances,
        hospitals,
        emergencies,
        priority_queue,
        history
    )

    assert emergencies["E002"]["status"] == "Dispatched"
    assert emergencies["E001"]["status"] == "Waiting"


# ============================================================
# TC05 - Same Priority FIFO
# FR5
# ============================================================

def test_TC05_same_priority_earlier_arrival_first():
    hospitals = {}

    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        }
    }

    emergencies = {
        "E001": {
            "emergency_id": "E001",
            "patient_location": "MG Road",
            "severity": "Critical",
            "priority": "High",
            "required_type": "Advanced",
            "traffic": "Low",
            "status": "Waiting",
            "arrival_order": 1,
            "selected_ambulance": None
        },
        "E002": {
            "emergency_id": "E002",
            "patient_location": "MG Road",
            "severity": "Critical",
            "priority": "High",
            "required_type": "Advanced",
            "traffic": "Low",
            "status": "Waiting",
            "arrival_order": 2,
            "selected_ambulance": None
        }
    }

    priority_queue = [
        (11, 1, "E001"),
        (11, 2, "E002")
    ]

    history = []

    Main.dispatch_ambulance(
        ambulances,
        hospitals,
        emergencies,
        priority_queue,
        history
    )

    assert emergencies["E001"]["status"] == "Dispatched"
    assert emergencies["E002"]["status"] == "Waiting"


# ============================================================
# TC06 - Busy Ambulance Not Selected
# FR6
# ============================================================

def test_TC06_busy_ambulance_not_selected():
    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Busy",
            "current_emergency": "E999"
        }
    }

    emergency = {
        "emergency_id": "E001",
        "patient_location": "MG Road",
        "severity": "Critical",
        "priority": "High",
        "required_type": "Advanced",
        "traffic": "Low"
    }

    result = Main.select_ambulance(ambulances, emergency)

    assert result[0] is None


# ============================================================
# TC07 - Find Nearby Ambulances
# FR7
# ============================================================

def test_TC07_nearby_ambulances():
    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        },
        "A03": {
            "ambulance_id": "A03",
            "hospital_id": "H02",
            "type": "Advanced",
            "location": "Indiranagar",
            "status": "Available",
            "current_emergency": None
        },
        "A04": {
            "ambulance_id": "A04",
            "hospital_id": "H02",
            "type": "Advanced",
            "location": "Whitefield",
            "status": "Returning",
            "current_emergency": None
        }
    }

    nearby = Main.find_nearby_ambulances(
        ambulances,
        "MG Road",
        10
    )

    assert len(nearby) == 2


# ============================================================
# TC08 - Traffic Response Time
# FR9
# ============================================================

def test_TC08_traffic_response_time():
    low_time = Main.estimate_response_time(5, "Low")
    heavy_time = Main.estimate_response_time(5, "Heavy")

    assert low_time == 9.0
    assert heavy_time == 26.7
    assert low_time < heavy_time


# ============================================================
# TC09 - Ambulance Type Suitability
# FR10
# ============================================================

def test_TC09_ambulance_type():
    assert Main.is_suitable("Advanced", "Advanced") is True
    assert Main.is_suitable("Advanced", "Basic") is True
    assert Main.is_suitable("Basic", "Advanced") is False
    assert Main.is_suitable("Basic", "Basic") is True


# ============================================================
# TC10 - Select Best Ambulance
# FR11
# ============================================================

def test_TC10_select_best_ambulance():
    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        },
        "A03": {
            "ambulance_id": "A03",
            "hospital_id": "H02",
            "type": "Advanced",
            "location": "Indiranagar",
            "status": "Available",
            "current_emergency": None
        }
    }

    emergency = {
        "emergency_id": "E001",
        "patient_location": "MG Road",
        "severity": "Critical",
        "priority": "High",
        "required_type": "Advanced",
        "traffic": "Low"
    }

    ambulance_id, distance, response_time = Main.select_ambulance(
        ambulances,
        emergency
    )

    # A01 is 3 km away and has the lower response time.
    assert ambulance_id == "A01"
    assert distance == 3.0
    assert response_time == 5.4


# ============================================================
# TC11 - Calculate Ambulance Bill
# FR15
# ============================================================

def test_TC11_calculate_bill():
    bill = Main.calculate_bill(
        5,
        "Critical",
        "Low",
        "B"
    )

    # 500 base
    # 160 distance (5 x 32)
    # 500 emergency
    # 200 traffic
    # 100 zone
    # Total = 1460
    assert bill == 1460.0


# ============================================================
# TC12 - Update Status and Location
# FR13 / FR14
# ============================================================

def test_TC12_update_status_location():
    hospitals = {
        "H01": {
            "hospital_id": "H01",
            "name": "City Hospital",
            "location": "MG Road",
            "total": 1,
            "available": 1,
            "busy": 0,
            "returning": 0,
            "at_hospital": 0
        }
    }

    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        }
    }

    Main.update_ambulance(
        ambulances,
        hospitals,
        "A01",
        "Returning",
        "MG Road"
    )

    assert ambulances["A01"]["status"] == "Returning"
    assert ambulances["A01"]["location"] == "MG Road"


# ============================================================
# TC13 - Dispatch History
# FR16
# ============================================================

def test_TC13_dispatch_history():
    history = []

    emergency = {
        "emergency_id": "E001",
        "patient_location": "MG Road",
        "severity": "Critical",
        "priority": "High",
        "required_type": "Advanced",
        "traffic": "Low",
        "status": "Dispatched"
    }

    ambulance = {
        "ambulance_id": "A03"
    }

    Main.save_history(
        history,
        emergency,
        ambulance,
        1460.0,
        5.0,
        9.0
    )

    assert len(history) == 1
    assert history[0]["emergency_id"] == "E001"
    assert history[0]["ambulance_id"] == "A03"
    assert history[0]["bill"] == 1460.0


# ============================================================
# TC14 - No Available Ambulance
# EC1
# ============================================================

def test_TC14_no_available_ambulance():
    hospitals = {}

    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Busy",
            "current_emergency": "E999"
        }
    }

    emergencies = {
        "E001": {
            "emergency_id": "E001",
            "patient_location": "MG Road",
            "severity": "Critical",
            "priority": "High",
            "required_type": "Advanced",
            "traffic": "Low",
            "status": "Waiting",
            "arrival_order": 1,
            "selected_ambulance": None
        }
    }

    priority_queue = [(11, 1, "E001")]
    history = []

    Main.dispatch_ambulance(
        ambulances,
        hospitals,
        emergencies,
        priority_queue,
        history
    )

    assert emergencies["E001"]["status"] == "Waiting"
    assert len(priority_queue) == 1


# ============================================================
# TC15 - Invalid Ambulance ID
# EC8
# ============================================================

def test_TC15_invalid_id(capsys):
    hospitals = {}
    ambulances = {}

    Main.update_ambulance(
        ambulances,
        hospitals,
        "A999",
        "Available",
        "MG Road"
    )

    output = capsys.readouterr().out

    assert "Invalid ambulance ID" in output


# ============================================================
# TC16 - Negative Distance
# EC10
# ============================================================

def test_TC16_negative_distance():
    bill = Main.calculate_bill(
        -5,
        "Critical",
        "Low",
        "A"
    )

    assert bill == 0.0


# ============================================================
# TC17 - Complete Integrated Workflow
# FR1-FR16
# ============================================================

def test_TC17_complete_workflow():

    # -------------------------
    # Step 1: Hospital
    # -------------------------

    hospitals = {
        "H01": {
            "hospital_id": "H01",
            "name": "City Hospital",
            "location": "MG Road",
            "total": 0,
            "available": 0,
            "busy": 0,
            "returning": 0,
            "at_hospital": 0
        }
    }

    # -------------------------
    # Step 2: Ambulances
    # -------------------------

    ambulances = {
        "A01": {
            "ambulance_id": "A01",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Koramangala",
            "status": "Available",
            "current_emergency": None
        },
        "A03": {
            "ambulance_id": "A03",
            "hospital_id": "H01",
            "type": "Advanced",
            "location": "Indiranagar",
            "status": "Available",
            "current_emergency": None
        }
    }

    Main.refresh_hospital_counts(
        hospitals,
        ambulances
    )

    # -------------------------
    # Step 3: Emergency
    # -------------------------

    emergencies = {
        "E001": {
            "emergency_id": "E001",
            "patient_location": "MG Road",
            "severity": "Critical",
            "priority": "High",
            "required_type": "Advanced",
            "traffic": "Low",
            "status": "Waiting",
            "arrival_order": 1,
            "selected_ambulance": None
        }
    }

    priority_queue = [
        (11, 1, "E001")
    ]

    history = []

    # -------------------------
    # Step 4: Dispatch
    # -------------------------

    Main.dispatch_ambulance(
        ambulances,
        hospitals,
        emergencies,
        priority_queue,
        history
    )

    # -------------------------
    # Step 5: Check result
    # -------------------------

    assert emergencies["E001"]["status"] == "Dispatched"
    assert emergencies["E001"]["selected_ambulance"] == "A01"
    assert ambulances["A01"]["status"] == "On the Way"

    # -------------------------
    # Step 6: History
    # -------------------------

    assert len(history) == 1
    assert history[0]["emergency_id"] == "E001"

    # -------------------------
    # Step 7: Update ambulance
    # -------------------------

    Main.update_ambulance(
        ambulances,
        hospitals,
        "A01",
        "At Patient Location",
        "MG Road"
    )

    assert ambulances["A01"]["status"] == "At Patient Location"
    assert ambulances["A01"]["location"] == "MG Road"
