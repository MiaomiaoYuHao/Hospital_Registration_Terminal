# patient.py

class Patient:
    _global_seq = 0  # Tracks global arrival order for FIFO

    def __init__(self, pid, name, age, initial_balance, is_walk_in=False, is_emergency=False):
        Patient._global_seq += 1
        self.seq = Patient._global_seq  
        
        self.pid = pid
        self.name = name
        self.age = age
        self.is_walk_in = is_walk_in       
        self.is_emergency = is_emergency   
        self.is_late = False               
        
        self.__balance = initial_balance  # Encapsulation

    def get_balance(self):
        return self.__balance

    def deduct_fee(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def mark_late(self):
        self.is_late = True
        Patient._global_seq += 1
        self.seq = Patient._global_seq

    def get_priority_tuple(self):
        """Core Priority Algorithm: 0(ER) > 1(Elder Online) > 2(Elder Walk-in) > 3(Online) > 4(Walk-in) > 5(Late)"""
        if self.is_emergency:
            category = 0
        elif self.is_late:
            category = 5
        elif self.age >= 65:
            category = 1 if not self.is_walk_in else 2
        else:
            category = 3 if not self.is_walk_in else 4
            
        return (category, self.seq)

    def __lt__(self, other):
        return self.get_priority_tuple() < other.get_priority_tuple()

    def __str__(self):
        status_str = "[MISSED TURN]" if self.is_late else ""
        elder_str = "[ELDERLY]" if self.age >= 65 else ""
        
        if self.is_emergency:
            type_str = "[EMERGENCY]"
        elif self.is_walk_in:
            type_str = "[Walk-in]"
        else:
            type_str = "[Online]"
            
        return f"{self.name} ({self.age}yo) {type_str} {elder_str} {status_str}"