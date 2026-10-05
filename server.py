# server.py
from doctor import Doctor, ExpertDoctor, EmergencyDoctor

class HospitalServerCore:
    total_handled = 0 

    @classmethod
    def record_visit(cls):
        cls.total_handled += 1
        return cls.total_handled

    def __init__(self):
        # Database of available doctors
        self.doctors = {
            "D1": Doctor("D1", "Dr. Smith", "General Med"),
            "E1": ExpertDoctor("E1", "Dr. House", "Pulmonology", "Chief Expert"),
            "EM1": EmergencyDoctor("EM1", "Dr. Carter", "Emergency Dept")
        }