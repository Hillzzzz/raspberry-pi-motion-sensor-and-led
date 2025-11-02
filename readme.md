# Raspberry Pi Motion → LED

A tiny, reliable Raspberry Pi project: a PIR motion sensor (HC-SR501) turns an LED on while motion is detected, and keeps it on for a short “hold” period after motion stops. Includes a `systemd` service and a simulation mode for CI/local dev.

## Features
- **gpiozero** implementation (works across Pi models)
- **Hold timer** (keeps LED on for `HOLD_SECONDS` after motion)
- **systemd** unit for boot-time startup
- **Simulation mode** (`SIMULATE=1`) to run without GPIO
- Minimal **CI** (pytest + ruff)

## Hardware
- Raspberry Pi (any with GPIO)
- HC-SR501 PIR sensor
- 1× LED + 330 Ω resistor
- Jumper wires, breadboard

### Wiring (BCM numbering)
- PIR **VCC** → Pi **5V** (pin 2 or 4)
- PIR **GND** → Pi **GND** (pin 6)
- PIR **OUT** → **GPIO17** (pin 11)

- LED **anode (+)** ← **GPIO18** (pin 12) through **330 Ω** resistor  
- LED **cathode (−)** → **GND** (pin 14)

