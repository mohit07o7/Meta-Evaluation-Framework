# APPENDIX A

# ARDUINO SOURCE CODE

```cpp
/*
 * Solar Powered Water Level Monitoring and Alert System
 * Project Code: 21CSP302L
 * Department of Computational Intelligence
 * SRM Institute of Science and Technology
 * 
 * Description: This program reads 8 water level probe inputs
 * (conditioned through 74LS08 AND gates), displays the current
 * water level on a 16x2 I2C LCD, and activates a buzzer alert
 * when the water reaches level 7 or above.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// LCD Configuration (I2C address 0x27, 16 columns, 2 rows)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pin Definitions — Water Level Probe Inputs (from AND gate outputs)
const int probePin[8] = {2, 3, 4, 5, 6, 7, 8, 9};

// Pin Definition — Buzzer Output (through BC547 transistor driver)
const int buzzerPin = 10;

// Alert threshold — buzzer activates at this level
const int ALERT_LEVEL = 7;

// Loop delay in milliseconds
const int LOOP_DELAY = 300;

// Variable to store the current water level (0 to 8)
int waterLevel = 0;

// Variable to store the previous water level (for change detection)
int previousLevel = -1;

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(9600);
  Serial.println("=== Solar Water Level Monitor ===");
  Serial.println("System Initializing...");
  
  // Configure probe input pins
  for (int i = 0; i < 8; i++) {
    pinMode(probePin[i], INPUT);
  }
  
  // Configure buzzer output pin
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);  // Buzzer OFF initially
  
  // Initialize LCD
  lcd.init();
  lcd.backlight();
  
  // Display startup message
  lcd.setCursor(0, 0);
  lcd.print("Water Level Mon.");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  
  delay(2000);  // Show startup message for 2 seconds
  lcd.clear();
  
  Serial.println("System Ready.");
}

void loop() {
  // Read all 8 probe inputs and count the number of HIGH signals
  waterLevel = 0;
  
  for (int i = 0; i < 8; i++) {
    if (digitalRead(probePin[i]) == HIGH) {
      waterLevel++;
    }
  }
  
  // Update display only if the level has changed (reduces LCD flicker)
  if (waterLevel != previousLevel) {
    updateDisplay(waterLevel);
    previousLevel = waterLevel;
    
    // Log to Serial Monitor
    Serial.print("Water Level Changed: ");
    Serial.print(waterLevel);
    Serial.println(" / 8");
  }
  
  // Buzzer Control — activate if water level >= ALERT_LEVEL
  if (waterLevel >= ALERT_LEVEL) {
    digitalWrite(buzzerPin, HIGH);  // Buzzer ON
  } else {
    digitalWrite(buzzerPin, LOW);   // Buzzer OFF
  }
  
  // Wait before next reading
  delay(LOOP_DELAY);
}

/*
 * Function: updateDisplay
 * Updates the 16x2 LCD with the current water level and status message.
 * 
 * Parameters:
 *   level - Current water level (0 to 8)
 */
void updateDisplay(int level) {
  lcd.clear();
  
  // Line 1: Water Level Reading
  lcd.setCursor(0, 0);
  lcd.print("Water Level:");
  lcd.print(level);
  lcd.print("/8");
  
  // Line 2: Status Message based on level
  lcd.setCursor(0, 1);
  
  if (level == 0) {
    lcd.print("TANK EMPTY!");
  } 
  else if (level >= 1 && level <= 3) {
    lcd.print("Status: LOW");
  } 
  else if (level >= 4 && level <= 6) {
    lcd.print("Status: MEDIUM");
  } 
  else if (level == 7) {
    lcd.print("ALERT!NEAR FULL");
  } 
  else if (level == 8) {
    lcd.print("TANK FULL!!");
  }
}


/*
 * CIRCUIT CONNECTIONS REFERENCE:
 * 
 * Arduino Pin D2  <-- AND Gate Output for Probe L1 (bottom)
 * Arduino Pin D3  <-- AND Gate Output for Probe L2
 * Arduino Pin D4  <-- AND Gate Output for Probe L3
 * Arduino Pin D5  <-- AND Gate Output for Probe L4
 * Arduino Pin D6  <-- AND Gate Output for Probe L5
 * Arduino Pin D7  <-- AND Gate Output for Probe L6
 * Arduino Pin D8  <-- AND Gate Output for Probe L7 (alert level)
 * Arduino Pin D9  <-- AND Gate Output for Probe L8 (top / full)
 * Arduino Pin D10 --> Buzzer (via 1k resistor to BC547 base)
 * Arduino Pin A4  --> LCD SDA (I2C Data)
 * Arduino Pin A5  --> LCD SCL (I2C Clock)
 * Arduino 5V      --> Power to logic gates, probes, LCD
 * Arduino GND     --> Common ground
 * 
 * POWER SUPPLY:
 * Solar Panel (12V 10W) --> Charge Controller --> 12V 7Ah Battery
 * Battery --> LM7805 Voltage Regulator --> 5V output to Arduino Vin
 * 
 * PROBE CIRCUIT (for each probe):
 * 5V --> 1k resistor --> Common Ground Probe (in tank bottom)
 * Probe Lx (in tank) --> 10k pull-down to GND
 * Probe Lx --> AND Gate Input A
 * AND Gate Input B --> tied to 5V (through 10k pull-up)
 * AND Gate Output --> Arduino Digital Pin
 */
```

---
---

# APPENDIX B

# CONFERENCE PUBLICATION

*[This section is to be filled with proof of conference paper presentation, if applicable]*

*[Insert acceptance letter / email screenshot]*

*[Insert conference certificate or best paper award, if received]*

---

<<To be updated with actual conference publication details upon acceptance>>

---
---

# APPENDIX C

# JOURNAL PUBLICATION

*[This section is to be filled with proof of journal publication, if applicable]*

*[Insert journal acceptance notification]*

*[Insert published paper first page / DOI link]*

---

<<To be updated with actual journal publication details upon acceptance>>

---
---

# APPENDIX D

# PLAGIARISM REPORT

*[This section must contain the Turnitin plagiarism report generated with the help of the project guide. The similarity index must be less than or equal to 10%.]*

*[Insert Turnitin report screenshot showing the similarity index]*

*[Insert Turnitin report showing the detailed similarity breakdown]*

---

<<To be generated using Turnitin through project guide before final submission>>
