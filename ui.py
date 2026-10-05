# ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import time

from patient import Patient
from server import HospitalServerCore

class HospitalAppUI:
    def __init__(self, root):
        self.root = root
        self.server = HospitalServerCore()
        
        self.first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", 
                            "Michael", "Linda", "David", "Elizabeth", "William", "Barbara"]
        self.last_initials = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M"]
        self.pid_counter = 1000
        self.listboxes = {} 
        
        self.setup_ui()
        self.log_sys("System Boot: Department triage queues initialized.")

    def setup_ui(self):
        ctrl_frame = tk.LabelFrame(self.root, text="📥 Mock Registration Terminal", font=("Arial", 10, "bold"))
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(ctrl_frame, text="📱 Online Appt", bg="#3498db", fg="white", 
                  command=lambda: self.sim_register(False)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(ctrl_frame, text="🚶 Walk-in", bg="#e67e22", fg="white", 
                  command=lambda: self.sim_register(True)).pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="👴 Elderly Priority", bg="#2ecc71", fg="white", 
                  command=lambda: self.sim_register(False, True)).pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="🚨 Emergency", bg="#e74c3c", fg="white", 
                  command=lambda: self.sim_register(False, False, True)).pack(side=tk.LEFT, padx=10)

        queues_frame = tk.LabelFrame(self.root, text="📊 Real-time Department Queues", font=("Arial", 10, "bold"))
        queues_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for doc_id, doc in self.server.doctors.items():
            doc_frame = tk.Frame(queues_frame)
            doc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            header_frame = tk.Frame(doc_frame, bg="#ecf0f1")
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=f"{doc.dept}\n{doc.name}", font=("Arial", 11, "bold"), bg="#ecf0f1").pack(pady=5)
            tk.Button(header_frame, text="🔊 Call Next Patient", bg="#9b59b6", fg="white", 
                      command=lambda d=doc_id: self.call_next_patient(d)).pack(pady=5, fill=tk.X, padx=20)
            
            lbox = tk.Listbox(doc_frame, font=("Arial", 10, "bold"), selectbackground="#bdc3c7")
            lbox.pack(fill=tk.BOTH, expand=True)
            self.listboxes[doc_id] = lbox

        self.log_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), height=8, bg="#1e1e1e", fg="#00ff00")
        self.log_area.pack(fill=tk.X, padx=10, pady=10)

    def log_sys(self, msg):
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_area.see(tk.END)

    def sim_register(self, is_walk_in=False, force_elder=False, is_emergency=False):
        self.pid_counter += 1
        name = f"{random.choice(self.first_names)} {random.choice(self.last_initials)}."
        if force_elder: name = "Elder " + name
        
        age = random.randint(65, 90) if force_elder else random.randint(18, 60)
        doc_id = "EM1" if is_emergency else random.choice(["D1", "E1"]) 
        age = random.randint(5, 80) if is_emergency else age
            
        patient = Patient(f"P{self.pid_counter}", name, age, 5000, is_walk_in, is_emergency)
        
        doctor = self.server.doctors[doc_id]
        if patient.deduct_fee(doctor.get_fee()):
            doctor.enqueue(patient) 
            source = "Walk-in" if is_walk_in else "Online"
            self.log_sys(f"📥 Registration Success: {patient.name} ({source}) -> Assigned to {doctor.dept}.")
            self.refresh_queues()

    def call_next_patient(self, doc_id):
        doctor = self.server.doctors[doc_id]
        if not doctor.queue:
            messagebox.showinfo("Notice", f"{doctor.name}'s queue is currently empty.")
            return

        patient = doctor.queue[0] 

        if not patient.is_late and random.random() < 0.20:
            doctor.queue.pop(0)
            patient.mark_late() 
            doctor.enqueue(patient) 
            self.log_sys(f"⚠️ [NO-SHOW] {patient.name} did not answer! Priority downgraded.")
        else:
            doctor.queue.pop(0)
            log = doctor.process_patient(patient) 
            self.server.record_visit()
            self.log_sys(f"✅ [CONSULTATION] {log}")
            
        self.refresh_queues()

    def refresh_queues(self):
        for doc_id, lbox in self.listboxes.items():
            lbox.delete(0, tk.END) 
            doctor = self.server.doctors[doc_id]
            for idx, p in enumerate(doctor.queue):
                lbox.insert(tk.END, f" {idx + 1}. {p}")
                if p.is_emergency: lbox.itemconfig(idx, {'fg': 'red', 'bg': '#ffe6e6'}) 
                elif p.is_late: lbox.itemconfig(idx, {'fg': '#7f8c8d'}) 
                elif p.age >= 65: lbox.itemconfig(idx, {'fg': '#27ae60'}) 
                elif p.is_walk_in: lbox.itemconfig(idx, {'fg': '#e67e22'}) 
                else: lbox.itemconfig(idx, {'fg': '#2980b9'})