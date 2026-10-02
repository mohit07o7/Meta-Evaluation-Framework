# CHAPTER 2

# LITERATURE SURVEY

## 2.1 Overview of the Research Area

Water level monitoring has been a subject of active research and development across the fields of instrumentation, embedded systems, and environmental engineering. The core objective of any water level monitoring system is straightforward — to measure or detect the height of water in a container, reservoir, or natural water body, and to communicate that information to a user or control system. However, the methods used to achieve this objective vary significantly in terms of complexity, accuracy, cost, and suitability for different applications.

At the broadest level, water level sensing techniques can be classified into two categories: contact-based methods and non-contact methods [9]. Contact-based methods involve sensors or probes that are physically in contact with the water. Examples include float switches, conductive probes, capacitive sensors, and pressure transducers. Non-contact methods measure the water level from a distance, without any physical contact with the liquid. Examples include ultrasonic sensors, infrared sensors, laser range finders, and radar-based systems.

**Float-Based Systems:** The simplest and most traditional form of water level measurement uses a float — a buoyant object that rises and falls with the water surface. The float is connected to a mechanical linkage or a magnetic reed switch that opens or closes an electrical circuit at predetermined levels. Float-based systems are inexpensive and easy to understand, but they suffer from mechanical wear, susceptibility to debris and sediment buildup, and limited resolution. Over time, the moving parts in a float mechanism can corrode or jam, leading to inaccurate readings or complete failure [10].

**Ultrasonic Sensors:** Ultrasonic level sensors work by emitting a burst of high-frequency sound waves (typically in the range of 20 to 200 kHz) from a transducer mounted above the water surface. The sound waves travel downward, reflect off the water surface, and return to the transducer. By measuring the time-of-flight — the time elapsed between transmission and reception of the echo — the sensor calculates the distance to the water surface and, consequently, the water level. Ultrasonic sensors offer non-contact measurement, which eliminates problems of corrosion and fouling. However, their accuracy can be affected by temperature variations (which alter the speed of sound), foam or turbulence on the water surface, and the geometry of the tank. The HC-SR04 ultrasonic sensor, widely used with Arduino, has a measurement range of 2 cm to 400 cm with an accuracy of approximately 3 mm [11].

*[Insert Figure 2.1: Ultrasonic Sensor Based Water Level System — A diagram showing an ultrasonic sensor mounted at the top of a tank, emitting sound waves towards the water surface]*

**Fig 2.1: Ultrasonic Sensor Based Water Level System**

**Capacitive Sensors:** Capacitive level sensing exploits the difference in dielectric constant between air and water. A capacitive probe, typically a coaxial tube or a pair of parallel conductors, is immersed in the tank. As the water level rises around the probe, the capacitance between the conductors increases because water has a much higher dielectric constant (approximately 80) compared to air (approximately 1). By measuring the capacitance, the water level can be determined with good resolution. Capacitive sensors provide continuous (analog) measurement and have no moving parts, but they require careful calibration, are sensitive to changes in water composition, and tend to be more expensive than simpler alternatives [12].

*[Insert Figure 2.2: Float Switch Mechanism — A cross-sectional diagram of a float switch inside a water tank]*

**Fig 2.2: Float Switch Mechanism**

**Conductive Probes:** Conductive sensing is one of the simplest and most cost-effective methods for detecting discrete water levels. It relies on the fact that tap water, groundwater, and most natural water sources contain dissolved minerals and salts that make them electrically conductive. Two metallic electrodes are placed in the water — one serves as a common reference (ground) and the other as a sensing probe. When the water touches both electrodes, it completes the circuit, allowing a small current to flow. This current, or the resulting voltage, is detected by a comparator or logic gate as a binary signal: water present (HIGH) or absent (LOW). While conductive sensing does not provide continuous level measurement like capacitive or ultrasonic methods, it is perfectly adequate for applications where knowing the water level at a few discrete points is sufficient. Its advantages include extremely low cost, simplicity of construction, no moving parts, and easy integration with digital electronics [13].

*[Insert Figure 2.3: Capacitive Level Sensing Principle — A diagram illustrating how capacitance changes with water level between two conductors]*

**Fig 2.3: Capacitive Level Sensing Principle**

**Pressure Transducers:** Hydrostatic pressure sensors measure the pressure exerted by the column of water above the sensor. Since pressure is directly proportional to the height of the water column (P = ρgh, where ρ is the density of the water, g is the acceleration due to gravity, and h is the height of the water column), the water level can be calculated from the pressure reading. Pressure transducers offer good accuracy and can provide continuous measurement, but they are significantly more expensive than conductive or float-based systems and are typically used in industrial or municipal applications rather than in domestic water tanks [14].


## 2.2 Existing Models and Frameworks

A substantial body of published work exists on the design and implementation of water level monitoring systems using various technologies. This section reviews the most relevant papers and projects that informed the design of the system presented in this report.

**1. Patel et al. (2016)** designed an Arduino-based water level controller that used simple conductive probes to detect water levels at three points — low, medium, and high. The system automatically controlled a water pump relay based on the detected level. When the tank was empty (no probes in contact with water), the pump was turned on. When the water reached the highest probe, the pump was switched off. While simple and functional, this system provided only three levels of resolution and did not include any display for real-time monitoring or any solar power capability [15].

**2. Kumar and Singh (2017)** developed an ultrasonic sensor-based water level monitoring system using an Arduino Mega and the HC-SR04 ultrasonic sensor. The system measured the distance between the sensor and the water surface and calculated the water level as a percentage of the tank's total depth. The level was displayed on a 16x2 LCD and also transmitted to a remote server via a Wi-Fi module (ESP8266) for monitoring through a web interface. This system offered continuous measurement and remote access, but the use of an ultrasonic sensor made it more expensive than conductive probe-based systems. The Wi-Fi module also required an active internet connection, which may not be available in rural areas. No solar power integration was implemented [16].

**3. Rashid et al. (2018)** proposed a water level monitoring system using a capacitive sensing array. The system used a series of copper electrodes arranged vertically inside a PVC pipe, which was placed inside the tank. Changes in capacitance at each electrode level were measured using a capacitance-to-digital converter IC. The digital output was processed by a PIC microcontroller, which displayed the level on a seven-segment display. This system provided higher resolution than conductive probe systems but was significantly more complex in terms of hardware and required precise calibration. The estimated cost was approximately three times that of a conductive probe system of equivalent capability [12].

*[Insert Figure 2.4: IoT-Based Water Monitoring Architecture — A system architecture diagram showing sensors connected to a microcontroller with cloud communication and mobile app interface]*

**Fig 2.4: IoT-Based Water Monitoring Architecture**

**4. Gaikwad and Kalshetty (2017)** designed an IoT-based water level monitoring system that combined an ultrasonic sensor with a GSM module. The system sent SMS alerts to the user's mobile phone when the tank was full or empty. The use of GSM ensured that alerts could be received even without internet connectivity, making it more suitable for rural areas than Wi-Fi-based solutions. However, the recurring cost of SMS messages and the requirement for a SIM card with an active plan added ongoing operational expenses [17].

**5. Oladipo (2019)** implemented a solar-powered automated water level controller using a PIC16F877A microcontroller. The system used float switches at two levels (minimum and maximum) to control a water pump relay. A 20W solar panel and a 12V battery provided power. This system is notable for its use of solar energy, which aligns with one of the key features of the project presented in this report. However, float switches have inherent limitations in terms of reliability and lifespan, and the system provided only two levels of measurement — significantly less granular than the eight levels offered by the conductive probe approach used in this project [18].

**6. Rao et al. (2020)** developed a smart water management system using Arduino and LoRa (Long Range) wireless communication. Multiple tanks in a neighbourhood were each fitted with ultrasonic sensors, and the level data from all tanks was collected by a central gateway using LoRa radio. The gateway uploaded the data to a cloud platform, enabling centralized monitoring of water resources across the community. While this system addressed the scalability challenge of monitoring multiple tanks, its complexity and cost made it more suitable for municipal or institutional deployment than for individual household use [19].

**7. Mishra and Sharma (2019)** explored the use of a resistive water level sensor combined with an ESP32 microcontroller for remote monitoring through the Blynk mobile application platform. The system displayed the water level on a smartphone app and provided push notifications for high and low levels. The use of a resistive sensor, which consists of interleaved copper traces on a PCB immersed in water, offered a compact form factor. However, resistive sensors are highly susceptible to corrosion and electrochemical degradation, often failing within a few months of continuous use in water [20].

*[Insert Figure 2.5: Comparison of Water Level Sensing Technologies — A radar chart or comparison infographic showing cost, accuracy, durability, complexity, and power consumption across different sensing methods]*

**Fig 2.5: Comparison of Water Level Sensing Technologies**

The following table provides a consolidated comparison of the sensing technologies and systems reviewed in this section.

| Author(s) | Year | Sensing Method | Controller | Display / Alert | Power Source | No. of Levels | IoT Capable |
|---|---|---|---|---|---|---|---|
| Patel et al. | 2016 | Conductive probes | Arduino Uno | Pump relay only | Mains AC | 3 | No |
| Kumar and Singh | 2017 | Ultrasonic (HC-SR04) | Arduino Mega | LCD + Web | Mains AC | Continuous | Yes (Wi-Fi) |
| Rashid et al. | 2018 | Capacitive array | PIC MCU | 7-segment display | Mains AC | 8+ | No |
| Gaikwad and Kalshetty | 2017 | Ultrasonic | Arduino Uno | SMS alerts | Mains AC | Continuous | Yes (GSM) |
| Oladipo | 2019 | Float switch | PIC16F877A | LED indicators | Solar | 2 | No |
| Rao et al. | 2020 | Ultrasonic | Arduino + LoRa | Cloud dashboard | Mains AC | Continuous | Yes (LoRa) |
| Mishra and Sharma | 2019 | Resistive sensor | ESP32 | Mobile app (Blynk) | Mains AC | Continuous | Yes (Wi-Fi) |
| **Proposed System** | **2026** | **Conductive probes** | **Arduino Uno** | **LCD + Buzzer** | **Solar** | **8** | **No (expandable)** |

**Table 2.1: Comparison of Water Level Sensing Technologies**


## 2.3 Limitations Identified from Literature Survey (Research Gaps)

The review of existing literature reveals several limitations and gaps that the proposed system aims to address.

**Gap 1 — Limited Resolution in Low-Cost Systems:** Systems that use conductive probes, which are the most affordable option, typically provide only two or three levels of measurement (e.g., low, medium, high). This coarse resolution gives the user limited information about the actual water level. The proposed system addresses this by increasing the number of conductive probes to eight, providing a much finer granularity of level indication while retaining the simplicity and low cost of the conductive sensing approach.

**Gap 2 — Dependence on Grid Electricity:** A majority of the systems reviewed in the literature depend on mains AC power for operation. This makes them unsuitable for deployment in rural or off-grid locations where power supply is unreliable. The proposed system eliminates this dependency entirely by incorporating a solar photovoltaic panel and rechargeable battery. The system can operate autonomously for extended periods, even during power outages or in areas without any grid connection.

**Gap 3 — Absence of User-Friendly Display:** Several low-cost systems use only LED indicators or pump relay control, without providing a clear numerical or graphical indication of the current water level to the user. The proposed system includes a 16x2 LCD display that shows the current level in an easy-to-read format (e.g., "Level: 5 / 8"), ensuring that the user always has precise information at a glance.

**Gap 4 — Lack of Active Alert Mechanism:** Many existing systems either monitor the water level passively (i.e., the user must actively check the display or indicator) or rely on remote notifications via SMS or internet, which have associated costs and connectivity requirements. The proposed system incorporates a locally-driven piezoelectric buzzer that produces a loud audible alert when the water level reaches the seventh probe, providing an immediate and cost-free notification to the user without requiring any external communication infrastructure.

**Gap 5 — Mechanical Reliability Concerns:** Float-based systems, while simple, are prone to mechanical failures. The moving parts — the float ball, the lever arm, the reed switch — are all subject to wear, corrosion, and jamming due to mineral deposits in the water. The proposed system uses stationary metallic probes with no moving parts, resulting in higher mechanical reliability and a longer operational life.

**Gap 6 — Complexity and Cost of Advanced Systems:** IoT-enabled systems with cloud connectivity, mobile apps, and continuous analog measurement offer sophisticated functionality but at a significantly higher cost and complexity. They require internet connectivity, subscription to cloud platforms, and often involve complex software setup. For the target use case of domestic water level monitoring in Indian households, such complexity is unnecessary and acts as a barrier to adoption. The proposed system strikes a balance between functionality and simplicity, providing adequate monitoring capability at a fraction of the cost.

**Table 2.3: Research Gaps Identified**

| Gap No. | Description | How Proposed System Addresses It |
|---|---|---|
| 1 | Low resolution (2–3 levels) in affordable systems | 8 conductive probes for fine granularity |
| 2 | Dependence on mains AC power | Solar panel + rechargeable battery |
| 3 | No user-friendly display | 16x2 LCD with clear level readout |
| 4 | No active local alert | Piezoelectric buzzer at 7th level |
| 5 | Mechanical failures in float systems | Stationary probes, no moving parts |
| 6 | High cost/complexity of IoT systems | Simple, affordable, standalone design |


## 2.4 Research Objectives

Based on the problem statement defined in Chapter 1 and the research gaps identified through the literature survey, the following research objectives have been formulated for this project:

**Objective 1:** To design and implement a multi-level water level sensing system using eight conductive probes that can reliably detect discrete water levels in a storage tank based on the electrical conductivity of water.

**Objective 2:** To design a signal conditioning circuit using digital logic gates (AND/OR gates) that converts the raw probe signals into clean, noise-free digital inputs suitable for processing by a microcontroller.

**Objective 3:** To program an Arduino Uno microcontroller to read the eight conditioned probe signals, determine the current water level, display the level information on a 16x2 LCD module, and trigger a buzzer alert when the water reaches the seventh level.

**Objective 4:** To design and integrate a solar power subsystem consisting of a photovoltaic panel, charge controller, rechargeable battery, and voltage regulator to power the entire monitoring system independently of grid electricity.

**Objective 5:** To build a working prototype of the complete system, test it under realistic conditions, and evaluate its performance in terms of detection accuracy, response time, display reliability, buzzer effectiveness, and power sustainability.

**Objective 6:** To document the design, implementation, testing, and results in a comprehensive project report, and to identify potential areas for future enhancement such as IoT integration, automatic pump control, and remote monitoring capabilities.


## 2.5 Product Backlog (Key User Stories with Desired Outcomes)

The product backlog defines the set of features and functionalities that the system must deliver, expressed as user stories in the Agile development format. Each user story describes a requirement from the perspective of the end user and specifies the desired outcome.

**Table 2.4: Product Backlog Items**

| Priority | User Story ID | User Story | Desired Outcome | Sprint |
|---|---|---|---|---|
| High | US-01 | As a user, I want the system to detect the current water level in my tank so that I know how much water is available. | The system accurately detects and displays water levels at 8 discrete points using conductive probes. | Sprint I |
| High | US-02 | As a user, I want the water level to be displayed on a screen so that I can read it easily from a distance. | A 16x2 LCD module displays the current level (e.g., "Level: 5/8") in clear, readable text. | Sprint II |
| High | US-03 | As a user, I want to hear an alarm when the tank is almost full so that I can switch off the pump in time. | A piezoelectric buzzer sounds continuously when the 7th probe is activated, alerting the user. | Sprint II |
| High | US-04 | As a user, I want the system to work without electricity from the grid so that it remains functional during power cuts. | The solar panel and battery provide uninterrupted power to the system at all times. | Sprint III |
| Medium | US-05 | As a user, I want the probe signals to be clean and noise-free so that the readings are reliable. | Logic gates condition the raw probe signals, eliminating noise and providing clean digital inputs. | Sprint I |
| Medium | US-06 | As a user, I want the system to be affordable and easy to install so that I can set it up without professional help. | Total component cost is under ₹1500, and the system can be assembled with basic tools. | All Sprints |
| Low | US-07 | As a user, I want the system to indicate if the tank is completely empty so that I know to turn on the pump. | The LCD displays "Tank Empty" when no probes detect water, prompting the user to start the pump. | Sprint II |
| Low | US-08 | As a user, I want the system to be weatherproof so that rain or humidity does not damage the electronics. | The Arduino and circuit board are housed in a waterproof enclosure. | Sprint III |

*[Insert Figure 2.6: Product Backlog Prioritization Chart — A visual chart showing the priority distribution of backlog items]*

**Fig 2.6: Product Backlog Prioritization Chart**


## 2.6 Plan of Action (Project Road Map)

The project was executed over a period of approximately fourteen weeks, divided into three sprints following the Agile Scrum methodology. Each sprint had a defined set of objectives, deliverables, and review points. The overall timeline is summarized below.

**Table 2.5: Project Timeline and Milestones**

| Week | Sprint | Activity | Deliverable |
|---|---|---|---|
| 1 – 2 | Pre-Sprint | Literature review, component selection, procurement | Literature survey document, component list |
| 3 – 4 | Sprint I | Design and test conductive probe sensing circuit | Working probe circuit with 8 levels |
| 5 | Sprint I | Design logic gate signal conditioning stage | Noise-free digital outputs from all 8 probes |
| 6 | Sprint I | Integrate probes with logic gates, test on breadboard | Functional sensor + logic gate unit |
| 7 | Sprint I Review | Sprint I demonstration and retrospective | Sprint I review document |
| 8 – 9 | Sprint II | Arduino programming — level detection and LCD display | Arduino code, LCD showing live levels |
| 10 | Sprint II | Buzzer alert integration and testing | Buzzer triggers at 7th level |
| 11 | Sprint II Review | Sprint II demonstration and retrospective | Sprint II review document |
| 12 | Sprint III | Solar panel, charge controller, battery integration | Standalone solar-powered unit |
| 13 | Sprint III | Final assembly, enclosure, field testing | Complete assembled prototype |
| 14 | Sprint III Review | Final demonstration, documentation, and submission | Complete project report and prototype |

*[Insert Figure 2.7: Project Road Map — Gantt Chart — A horizontal Gantt chart showing the timeline of all sprints and activities across the 14-week project duration]*

**Fig 2.7: Project Road Map — Gantt Chart**

The Agile Scrum methodology was chosen for this project because of its iterative nature, which allows for continuous testing and refinement of each subsystem before integrating them into the final product. At the end of each sprint, a review was conducted to evaluate the outcomes against the planned objectives, and a retrospective was held to identify what went well, what could be improved, and what adjustments were needed for the next sprint. This approach ensured that issues were identified and resolved early, reducing the risk of integration problems during the final assembly.

**Component Procurement Plan:**

The following components were identified and procured during the pre-sprint phase based on the system design requirements:

| Component | Specification | Quantity | Approx. Cost (₹) |
|---|---|---|---|
| Arduino Uno R3 | ATmega328P, 14 digital I/O pins, 5V operating voltage | 1 | 450 |
| 16x2 LCD Display | HD44780 compatible, I2C backpack | 1 | 120 |
| Stainless Steel Rods (Probes) | 3 mm diameter, 150 mm length, food-grade SS304 | 9 (8 + 1 ground) | 90 |
| Logic Gate IC — 74LS08 | Quad 2-input AND gate | 2 | 30 |
| Piezoelectric Buzzer | 5V active buzzer, 85 dB at 10 cm | 1 | 25 |
| NPN Transistor — BC547 | For buzzer driver circuit | 1 | 5 |
| Resistors (10 kΩ) | Pull-down resistors for probe inputs | 8 | 10 |
| Resistors (1 kΩ) | Current limiting for logic gate inputs | 8 | 10 |
| Solar Panel | 12V, 10W polycrystalline | 1 | 350 |
| PWM Charge Controller | 6V/12V, 5A | 1 | 180 |
| Rechargeable Battery | 12V, 7Ah sealed lead-acid (SLA) | 1 | 550 |
| LM7805 Voltage Regulator | 5V, 1A output | 1 | 15 |
| Connecting Wires | Assorted jumper wires and hookup wire | 1 set | 50 |
| Breadboard | 830 tie-point solderless breadboard | 1 | 80 |
| Waterproof Enclosure | ABS plastic, IP65 rated, 200x150x75 mm | 1 | 150 |
| **Total** | | | **≈ ₹2,115** |

The total estimated cost of the prototype is approximately two thousand one hundred and fifteen rupees, which is well within the budget constraints of a student project and significantly lower than most commercial water level controllers available in the Indian market.
