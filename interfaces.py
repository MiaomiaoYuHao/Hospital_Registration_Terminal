from abc import ABC, abstractmethod

class MedicalService(ABC):
    """
    Abstract Base Class (ADT): Defines the standard interface for medical services.
    Forces any child class to implement get_fee() and process_patient().
    """
    @abstractmethod
    def get_fee(self) -> float:
        pass

    @abstractmethod
    def process_patient(self, patient) -> str:
        pass