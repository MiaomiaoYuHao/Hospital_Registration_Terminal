# doctor.py
from interfaces import MedicalService
from patient import Patient

class Doctor(MedicalService):
    def __init__(self, doc_id, name, dept):
        self.doc_id = doc_id
        self.name = name
        self.dept = dept
        self.queue = [] 

    def enqueue(self, patient: Patient):
        self.queue.append(patient)
        self.queue.sort() # Triggers the priority sorting algorithm

    def get_fee(self):
        return 50.0 

    def process_patient(self, patient: Patient):
        return f"👨‍⚕️ [{self.dept}] {self.name} is consulting: {patient.name}"

class ExpertDoctor(Doctor):
    def __init__(self, doc_id, name, dept, title):
        super().__init__(doc_id, name, dept)
        self.title = title

    def get_fee(self):
        return 150.0 

    def process_patient(self, patient: Patient):
        return f"🌟 [{self.title}] {self.name} is performing a deep consultation for {patient.name}"

class EmergencyDoctor(Doctor):
    def get_fee(self):
        return 200.0 

    def process_patient(self, patient: Patient):
        return f"🚨 [ER] {self.name} is performing emergency resuscitation on {patient.name}!"