# CHAPTER 1

# INTRODUCTION

## 1.1 Introduction to Project

Water is one of the most essential natural resources for the sustenance of life on earth. Despite covering nearly seventy-one percent of the planet's surface, only about two and a half percent of the earth's water is freshwater, and a significant fraction of that remains locked in glaciers and ice caps [1]. The accessible freshwater available for domestic, agricultural, and industrial use is therefore extremely limited. In countries like India, where the population continues to grow at a rapid pace and urbanization is expanding, the demand for clean and usable water has never been higher. According to a report by NITI Aayog (2018), India faces one of the worst water crises in its history, with nearly six hundred million people experiencing high to extreme water stress [2].

In residential and semi-urban settings, overhead water storage tanks are the most widely used method for ensuring a continuous supply of water. These tanks are filled by electric pumps that draw water from underground borewells or municipal supply lines. However, a common and persistent problem associated with this arrangement is the lack of any reliable mechanism to monitor the level of water inside these tanks. In many households, the water pump is turned on manually and left running without supervision. Since the tank is typically installed on the roof or at an elevated position, the user has no direct visibility of the water level. This leads to two undesirable outcomes. First, if the pump is left running for too long, the tank overflows, resulting in substantial water wastage. Second, if the pump is not turned on in time, the tank runs empty, causing an interruption in water supply during critical hours.

The problem of water overflow from storage tanks is not trivial. Studies have estimated that a standard household overhead tank of one thousand litres capacity, when left to overflow for just thirty minutes, can waste upwards of two hundred litres of water [3]. Over weeks and months, this wastage accumulates into a significant volume, particularly in water-scarce regions where every litre counts. Beyond the waste of water itself, there is also the wasted electricity consumed by the pump during the overflow period. In rural areas where electricity supply is erratic and power costs are a concern, this inefficiency adds an additional burden on families.

*[Insert Figure 1.1: Conventional Water Level Indicator Setup — A photograph or illustration showing a traditional overhead tank with a manual pump switch and no monitoring mechanism]*

**Fig 1.1: Conventional Water Level Indicator Setup**

Several commercial water level controllers are available in the market, ranging from simple float-based switches to electronic controllers. However, many of these solutions are either too expensive for widespread adoption in rural India, or they depend on continuous grid electricity for operation. Float-based systems are prone to mechanical failure due to the moving parts involved, while purely electronic systems can be unreliable in areas with fluctuating or absent power supply. There exists, therefore, a genuine need for a water level monitoring system that is affordable, reliable, easy to maintain, and capable of operating independently of the power grid.

This project presents the design and development of a Solar Powered Water Level Monitoring and Alert System that addresses all of the challenges mentioned above. The system uses conductive metal probes inserted at eight predefined vertical positions inside the water tank. These probes exploit the natural electrical conductivity of water — when the water level reaches a particular probe, it completes a circuit between that probe and a common ground electrode placed at the base of the tank. This event generates a detectable electrical signal that is interpreted as a logic HIGH by the downstream circuitry. Each of the eight probe outputs is passed through a dedicated digital logic gate, which acts as a signal conditioner and discrete level indicator.

The conditioned signals from the logic gates are read by an Arduino Uno microcontroller, which is the central processing unit of the system. The Arduino firmware continuously scans the eight input channels and determines how many probes are currently in contact with water. Based on this count, the microcontroller calculates the approximate water level as a fraction of the tank's total capacity and displays it on a 16x2 LCD screen in a format that is easy for the user to understand. When the water reaches the seventh level (probe L7), which corresponds to approximately eighty-seven percent of the tank's capacity, the Arduino activates a piezoelectric buzzer to produce a loud audible alarm. This alert notifies the user to switch off the pump and prevents overflow.

The entire system is powered by a standalone solar energy unit comprising a photovoltaic panel, a charge controller, and a rechargeable battery. The solar panel generates electricity from sunlight during the day, and the charge controller regulates this energy to safely charge the battery. The battery, in turn, provides a stable power supply to the Arduino and all peripheral components through a voltage regulator. This solar-powered design makes the system entirely self-sufficient and eliminates any dependence on grid electricity. It is particularly well-suited for deployment in rural and remote areas where power supply is inconsistent.

The key contributions of this project include the integration of a simple yet effective conductive sensing technique with digital logic processing and microcontroller-based intelligence, all powered by a clean and renewable energy source. The system is designed with an emphasis on affordability, ease of installation, and low maintenance. The total component cost of the prototype is well within the reach of an average household, and the modular design allows for easy replacement of individual parts if needed.


## 1.2 Problem Statement and Description

The efficient management of water in domestic storage tanks remains a significant challenge in many parts of India and other developing nations. The fundamental problem can be stated as follows: there is an absence of affordable, reliable, and energy-independent systems for monitoring the water level in overhead tanks and providing timely alerts to prevent overflow and dry-running of pumps.

This problem has several dimensions that deserve detailed examination.

**Water Wastage:** The Central Ground Water Board of India has reported that groundwater levels in several states have been declining steadily over the past two decades [4]. In this context, the wastage of water due to tank overflow is not merely an inconvenience but a direct contributor to the depletion of an already scarce resource. In apartment complexes and multi-storey buildings, where large-capacity tanks serve multiple families, overflow events can result in the loss of hundreds of litres of water every day. This is water that has been pumped from underground aquifers using electric energy, and its loss represents a waste of both natural and economic resources.

| Parameter | Data |
|---|---|
| Average daily household water consumption in India | 135 litres per person [5] |
| Estimated water wasted due to tank overflow per household per month | 600 – 1200 litres |
| Percentage of Indian households without any water level indicator | Over 70% (estimated) |
| Average cost of electricity wasted due to pump running during overflow | ₹150 – ₹300 per month |

**Table 1.1: Global Water Wastage Statistics**

**Electricity Wastage:** The water pump used to fill overhead tanks is one of the significant electricity consumers in a typical household. A standard half-horsepower submersible pump draws approximately 370 watts of power. If this pump is left running for an unnecessary thirty minutes during every filling cycle, and if the tank is filled twice a day, the wasted electricity over a month amounts to approximately 11 kilowatt-hours. At an average electricity tariff of ₹7 per unit, this translates to a financial loss of roughly ₹77 per month per household. While this may seem small in isolation, the aggregate impact across millions of households is enormous.

*[Insert Figure 1.2: Water Wastage Statistics in Indian Households — A bar chart or infographic showing statistics on household water wastage, pump electricity consumption, and percentage of homes without water level monitoring]*

**Fig 1.2: Water Wastage Statistics in Indian Households**

**Pump Damage:** Submersible and centrifugal pumps are designed to operate while submerged in water or while water is flowing through them. When a tank runs empty and the pump is not switched off, it continues to run in a dry state. Dry running causes excessive heat buildup in the pump motor, damages the mechanical seals, and can lead to permanent motor burnout. The cost of repairing or replacing a damaged pump far exceeds the cost of installing a simple monitoring system.

**Lack of Awareness in Real Time:** In a typical household, the water tank is installed on the rooftop or on an elevated platform, well above the line of sight. The user has no way of knowing the current water level unless they physically climb up and look inside the tank. This is impractical, especially for elderly residents and in multi-storey buildings. The lack of real-time information means that users tend to follow a fixed schedule for running the pump — for instance, running it every morning for forty-five minutes — regardless of whether the tank is half full or nearly empty. This leads to either overflow or shortage, depending on the day's water consumption.

**Power Dependency of Existing Solutions:** Many electronic water level controllers available in the Indian market operate on mains electricity (230V AC) and require continuous power to function. In rural and semi-urban areas, where power cuts of four to eight hours per day are common, these systems become non-functional precisely when monitoring is needed the most. Battery-backed systems exist, but they add to the cost and require periodic battery replacement.

The problem statement for this project can therefore be formally expressed as: *To design and implement a low-cost, solar-powered water level monitoring and alert system that uses conductive probes and digital logic gates to detect water levels in a storage tank, processes the level information using an Arduino microcontroller, displays the level on an LCD screen, and generates an audible alert when the tank is nearly full.*


## 1.3 Motivation

The motivation behind this project stems from a combination of personal observation, environmental responsibility, and the desire to apply academic knowledge in embedded systems to solve a tangible real-world problem.

**Personal Observation:** Growing up in a household that depends on an overhead water tank for its daily supply, the authors have personally experienced the inconvenience and waste associated with manual water level management. The routine of running the pump in the morning, climbing to the terrace to check whether the tank is full, and then rushing down to switch off the pump is a daily exercise that most Indian families are familiar with. On numerous occasions, the pump has been left running during periods of inattention — while cooking, attending phone calls, or simply forgetting — leading to water spilling over the tank's edges and flowing down the walls of the building. Each such incident reinforces the need for a simple, automated solution that can provide timely information and alerts.

**Environmental Responsibility:** Water conservation is no longer a matter of choice but a necessity. The World Health Organization (WHO) has projected that by the year 2025, half of the world's population will be living in water-stressed areas [6]. India, in particular, faces a grim outlook. The Composite Water Management Index published by NITI Aayog in 2018 warned that twenty-one major Indian cities, including Delhi, Bengaluru, Chennai, and Hyderabad, will run out of groundwater by 2030, affecting access for nearly one hundred million people [2]. In this scenario, every effort to reduce water wastage — no matter how small at the individual level — contributes to a larger collective impact. A water level monitoring system that prevents overflow in even a fraction of the country's households could save millions of litres of water annually.

**Renewable Energy Integration:** The decision to power the system with solar energy was motivated by two factors. First, the practical limitation that many potential deployment sites — especially in rural India — do not have reliable access to grid electricity. A system that requires mains power would be of limited use in these areas. Second, the broader imperative of reducing carbon emissions and dependence on fossil fuels. India's electricity generation is still heavily reliant on coal-fired thermal power plants, which are major contributors to greenhouse gas emissions. By using solar power, this project demonstrates that even small-scale embedded systems can be designed to operate on clean energy, thereby contributing to the country's commitment to reduce its carbon footprint under the Paris Agreement [7].

**Academic and Technical Interest:** From a technical perspective, this project brings together several domains of knowledge covered in the undergraduate computer science and engineering curriculum. The sensing mechanism involves basic principles of physics — electrical conductivity and circuit completion. The logic gate stage draws on digital electronics and Boolean algebra. The microcontroller programming touches on embedded systems, real-time processing, and hardware-software interfacing. The solar power unit involves concepts of renewable energy systems, battery management, and voltage regulation. By integrating all of these into a single working prototype, this project provides a hands-on learning experience that goes beyond theoretical coursework.

**Social Impact and Scalability:** Perhaps the most compelling motivation is the potential for social impact. The system described in this report is deliberately designed to be simple and inexpensive. The total component cost of the prototype is less than fifteen hundred rupees, making it affordable even for low-income households. The use of widely available components — standard Arduino boards, common logic gate ICs, stainless steel rods as probes, and off-the-shelf solar panels — means that the system can be assembled and maintained without specialized tools or expertise. This makes it a viable candidate for deployment at scale, whether through government rural development programs, non-governmental organizations, or community initiatives.


## 1.4 Sustainable Development Goal of the Project

This project is closely aligned with the United Nations Sustainable Development Goals (SDGs), particularly SDG 6: Clean Water and Sanitation. The United Nations General Assembly adopted the 2030 Agenda for Sustainable Development in September 2015, establishing seventeen goals intended to guide global development efforts towards a more equitable, prosperous, and sustainable future [8]. SDG 6 specifically calls for ensuring the availability and sustainable management of water and sanitation for all. Among its key targets are:

- **Target 6.4:** By 2030, substantially increase water-use efficiency across all sectors and ensure sustainable withdrawals and supply of freshwater to address water scarcity and substantially reduce the number of people suffering from water scarcity.
- **Target 6.a:** By 2030, expand international cooperation and capacity-building support to developing countries in water and sanitation-related activities and programmes, including water harvesting, desalination, water efficiency, wastewater treatment, recycling and reuse technologies.

*[Insert Figure 1.3: UN Sustainable Development Goal 6 — Clean Water and Sanitation — The official SDG 6 icon or an infographic showing the key targets of SDG 6]*

**Fig 1.3: UN Sustainable Development Goal 6 — Clean Water and Sanitation**

The solar-powered water level monitoring system contributes to SDG 6 in a direct and measurable way. By preventing tank overflow, the system reduces domestic water wastage, which is one of the simplest and most impactful steps towards improving water-use efficiency at the household level. The target of reducing the number of people suffering from water scarcity is also served indirectly — when less water is wasted, more water remains available for others in the community, particularly in areas served by shared water sources such as borewells and community taps.

Beyond SDG 6, the project also touches on several other SDGs:

- **SDG 7 — Affordable and Clean Energy:** The use of a solar photovoltaic panel as the primary power source demonstrates the practical application of affordable and clean energy technology in everyday devices. By running an embedded system entirely on solar power, the project illustrates that renewable energy is not limited to large-scale power generation but can also be effectively harnessed for small-scale, distributed applications.

- **SDG 9 — Industry, Innovation and Infrastructure:** The project represents an innovative application of embedded systems technology to infrastructure (water storage systems). The use of an Arduino microcontroller, combined with simple sensing hardware and digital logic, showcases how innovation can be achieved with accessible and open-source platforms, promoting inclusive and sustainable industrialization.

- **SDG 11 — Sustainable Cities and Communities:** Efficient water management is a cornerstone of sustainable urban and rural development. By providing households with a tool to monitor and control their water usage, this system contributes to making communities more sustainable and resilient to water-related challenges.

- **SDG 12 — Responsible Consumption and Production:** The project promotes responsible consumption of water by making users aware of their tank's water level in real time. The audible alert at near-full capacity actively encourages users to act responsibly and turn off the pump before overflow occurs.

- **SDG 13 — Climate Action:** By using solar energy instead of grid electricity (which in India is predominantly generated from coal), the system reduces indirect carbon emissions associated with powering the monitoring equipment. While the emissions avoided by a single device are small, the principle of designing carbon-neutral embedded systems is significant and scalable.

In summary, this project does not exist in isolation as a mere technical exercise. It is rooted in the broader context of global sustainability challenges and demonstrates how engineering solutions, even at a small scale, can contribute meaningfully to the goals set by the international community.
