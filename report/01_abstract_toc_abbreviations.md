# ABSTRACT

Water scarcity and its inefficient management remain pressing concerns across the globe, particularly in developing nations where domestic and agricultural water storage plays a vital role. Overhead water tanks, widely used in residential and rural settings, often suffer from overflow or run dry due to the absence of reliable monitoring mechanisms. Manual inspection of water levels is not only inconvenient but also leads to considerable wastage of water and electricity used for pumping. This project presents the design and implementation of a Solar Powered Water Level Monitoring and Alert System that addresses these challenges using a combination of conductive water level sensing, digital logic gates, and an Arduino-based microcontroller platform.

The proposed system employs eight metallic probes placed at predetermined vertical positions inside a water storage tank. These probes work on the principle of electrical conductivity — when water reaches a probe, it completes a circuit through the water medium, generating a logic HIGH signal. Each probe signal is routed through dedicated logic gates that serve as discrete level indicators. As the water rises in the tank, probes are sequentially activated, providing a step-wise digital representation of the water level at any given time. The conditioned digital signals are fed into an Arduino Uno microcontroller, which reads and processes them to compute the current water level. The microcontroller then drives a 16x2 LCD display module that presents real-time level information in a user-friendly format. When the water reaches the 7th probe (indicating near-full capacity), the Arduino triggers a piezoelectric buzzer to produce an audible alarm, alerting the user to take corrective action such as switching off the water pump.

A distinguishing feature of this system is its complete reliance on solar energy for power. A photovoltaic solar panel converts sunlight into electrical energy, which is regulated through a charge controller and stored in a rechargeable lead-acid battery. A voltage regulator then supplies a stable 5V DC output to power the entire electronic subsystem. This makes the system well-suited for rural and remote locations where grid electricity is unreliable or absent. The solar-powered design also reduces operational costs and environmental impact, aligning with global sustainability goals.

Experimental testing of the prototype confirmed reliable detection across all eight levels under standard tap water conditions. The LCD display correctly reflected the water level, and the buzzer alert triggered consistently at the 7th level. The system demonstrated stable operation under solar power during daylight hours and maintained functionality through the battery during cloudy intervals. Limitations including probe corrosion over extended use and reduced sensitivity in distilled or low-conductivity water were also identified and discussed.

**Keywords:** Water level monitoring, Arduino Uno, solar energy, conductive sensing, logic gates, LCD display, buzzer alert, embedded systems, renewable energy

---
---

# TABLE OF CONTENTS

| | | Page No. |
|---|---|---|
| | ABSTRACT | v |
| | TABLE OF CONTENTS | vi |
| | LIST OF FIGURES | vii |
| | LIST OF TABLES | viii |
| | ABBREVIATIONS | ix |

| Chapter No. | Title | Page No. |
|---|---|---|
| **1** | **INTRODUCTION** | **1** |
| 1.1 | Introduction to Project | 1 |
| 1.2 | Problem Statement and Description | 3 |
| 1.3 | Motivation | 5 |
| 1.4 | Sustainable Development Goal of the Project | 7 |
| **2** | **LITERATURE SURVEY** | **9** |
| 2.1 | Overview of the Research Area | 9 |
| 2.2 | Existing Models and Frameworks | 11 |
| 2.3 | Limitations Identified from Literature Survey (Research Gaps) | 15 |
| 2.4 | Research Objectives | 17 |
| 2.5 | Product Backlog (Key User Stories with Desired Outcomes) | 18 |
| 2.6 | Plan of Action (Project Road Map) | 20 |
| **3** | **SPRINT PLANNING AND EXECUTION METHODOLOGY** | **23** |
| 3.1 | Sprint I — Sensor Interface and Logic Gate Design | 23 |
| | 3.1.1 Objectives with User Stories of Sprint I | 23 |
| | 3.1.2 Functional Document | 25 |
| | 3.1.3 Architecture Document | 27 |
| | 3.1.4 Outcome of Objectives / Result Analysis | 29 |
| | 3.1.5 Sprint Retrospective | 30 |
| 3.2 | Sprint II — Microcontroller Integration, Display and Alert System | 31 |
| | 3.2.1 Objectives with User Stories of Sprint II | 31 |
| | 3.2.2 Functional Document | 33 |
| | 3.2.3 Architecture Document | 35 |
| | 3.2.4 Outcome of Objectives / Result Analysis | 36 |
| | 3.2.5 Sprint Retrospective | 37 |
| 3.3 | Sprint III — Solar Power Integration and Final Assembly | 38 |
| | 3.3.1 Objectives with User Stories of Sprint III | 38 |
| | 3.3.2 Functional Document | 39 |
| | 3.3.3 Architecture Document | 40 |
| | 3.3.4 Outcome of Objectives / Result Analysis | 41 |
| | 3.3.5 Sprint Retrospective | 42 |
| **4** | **RESULTS AND DISCUSSIONS** | **43** |
| 4.1 | Project Outcomes | 43 |
| 4.2 | Performance Evaluation | 44 |
| 4.3 | Comparative Analysis | 46 |
| 4.4 | Testing Results | 47 |
| **5** | **CONCLUSION AND FUTURE ENHANCEMENT** | **49** |
| 5.1 | Conclusion | 49 |
| 5.2 | Future Enhancement | 50 |
| | REFERENCES | 52 |
| | APPENDIX A — Arduino Source Code | 55 |
| | APPENDIX B — Conference Publication | 59 |
| | APPENDIX C — Journal Publication | 60 |
| | APPENDIX D — Plagiarism Report | 61 |

---
---

# LIST OF FIGURES

| Figure No. | Title | Page No. |
|---|---|---|
| 1.1 | Conventional Water Level Indicator Setup | 2 |
| 1.2 | Water Wastage Statistics in Indian Households | 4 |
| 1.3 | UN Sustainable Development Goal 6 — Clean Water and Sanitation | 7 |
| 2.1 | Ultrasonic Sensor Based Water Level System | 10 |
| 2.2 | Float Switch Mechanism | 11 |
| 2.3 | Capacitive Level Sensing Principle | 12 |
| 2.4 | IoT-Based Water Monitoring Architecture | 13 |
| 2.5 | Comparison of Water Level Sensing Technologies | 14 |
| 2.6 | Product Backlog Prioritization Chart | 19 |
| 2.7 | Project Road Map — Gantt Chart | 21 |
| 3.1 | Conductive Probe Sensing Principle | 24 |
| 3.2 | Logic Gate Configuration for Level Detection | 26 |
| 3.3 | Sensor Interface Circuit Schematic | 27 |
| 3.4 | System Block Diagram | 28 |
| 3.5 | Sprint I Test Results — Probe Response | 29 |
| 3.6 | Arduino Uno Pin Mapping | 32 |
| 3.7 | LCD Display Interface Wiring | 34 |
| 3.8 | Complete Circuit Schematic | 35 |
| 3.9 | Buzzer Alert Trigger Logic Flowchart | 36 |
| 3.10 | Solar Power Subsystem Block Diagram | 39 |
| 3.11 | Charge Controller and Battery Wiring | 40 |
| 3.12 | Assembled Prototype — Top View | 41 |
| 3.13 | Assembled Prototype — Tank with Probes | 42 |
| 4.1 | Water Level Detection Accuracy Graph | 44 |
| 4.2 | Response Time at Different Levels | 45 |
| 4.3 | Solar Panel Output Voltage over 12 Hours | 45 |
| 4.4 | Battery Discharge Curve During Operation | 46 |
| 4.5 | Comparison Chart — Proposed vs Existing Systems | 47 |
| 4.6 | LCD Display Output at Various Water Levels | 48 |

---
---

# LIST OF TABLES

| Table No. | Title | Page No. |
|---|---|---|
| 1.1 | Global Water Wastage Statistics | 3 |
| 2.1 | Comparison of Water Level Sensing Technologies | 14 |
| 2.2 | Summary of Literature Reviewed | 15 |
| 2.3 | Research Gaps Identified | 16 |
| 2.4 | Product Backlog Items | 18 |
| 2.5 | Project Timeline and Milestones | 20 |
| 3.1 | Sprint I User Stories and Acceptance Criteria | 23 |
| 3.2 | Logic Gate Truth Table for Level Detection | 26 |
| 3.3 | Sprint I Test Cases and Results | 29 |
| 3.4 | Arduino Pin Assignment Table | 32 |
| 3.5 | Sprint II User Stories and Acceptance Criteria | 31 |
| 3.6 | LCD Display Modes and Messages | 34 |
| 3.7 | Sprint II Test Cases and Results | 36 |
| 3.8 | Solar Panel Specifications | 39 |
| 3.9 | Battery Specifications | 40 |
| 3.10 | Sprint III Test Cases and Results | 41 |
| 4.1 | Detection Accuracy across All Eight Levels | 44 |
| 4.2 | Power Consumption Breakdown | 45 |
| 4.3 | Comparative Analysis with Existing Systems | 46 |
| 4.4 | Functional Testing Summary | 47 |

---
---

# ABBREVIATIONS

| Abbreviation | Full Form |
|---|---|
| AC | Alternating Current |
| ADC | Analog to Digital Converter |
| DC | Direct Current |
| GPIO | General Purpose Input Output |
| I2C | Inter-Integrated Circuit |
| IC | Integrated Circuit |
| IDE | Integrated Development Environment |
| IoT | Internet of Things |
| LCD | Liquid Crystal Display |
| LED | Light Emitting Diode |
| MCU | Microcontroller Unit |
| MPPT | Maximum Power Point Tracking |
| PCB | Printed Circuit Board |
| PV | Photovoltaic |
| PWM | Pulse Width Modulation |
| SDG | Sustainable Development Goal |
| SLA | Sealed Lead Acid |
| TTL | Transistor-Transistor Logic |
| UART | Universal Asynchronous Receiver Transmitter |
| USB | Universal Serial Bus |
| UV | Ultraviolet |
| WHO | World Health Organization |
