# Hospital Registration Terminal

A small **hospital registration & department queue scheduling system** written in pure
Python with a Tkinter GUI. It was originally built as a course project to demonstrate
object-oriented design (abstraction, inheritance, polymorphism, encapsulation) applied to
a realistic hospital reception workflow.

## Features

- Mock registration of walk-in and emergency patients
- Department triage queues (General Medicine, Pulmonology, Emergency)
- Doctor types with different fees and service behaviour
- FIFO ordering based on global arrival sequence
- Live queue view and system log in a Tkinter interface

## Project Structure

| File | Responsibility |
| --- | --- |
| `main.py` | Application entry point; creates the Tk root window. |
| `ui.py` | Tkinter UI: registration panel, queues, log output. |
| `server.py` | `HospitalServerCore` - doctor registry and visit counter. |
| `doctor.py` | `Doctor` / `ExpertDoctor` / `EmergencyDoctor` classes. |
| `patient.py` | `Patient` model with FIFO sequence tracking. |
| `interfaces.py` | `MedicalService` abstract base class (ADT). |

## Requirements

- Python 3.8+
- Tkinter (bundled with most CPython distributions)

No third-party packages are required.

## Run

```bash
python main.py
```

## License

Released under the MIT License. See `LICENSE`.