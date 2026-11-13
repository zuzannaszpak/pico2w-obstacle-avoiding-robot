# pico2w-obstacle-avoiding-robot
Autonomous obstacle-avoiding robot car built with a Raspberry Pi Pico 2 W, HC-SR04 ultrasonic sensor, SG90 servo, and L298N motor driver, programmed in MicroPython.

## How It Works

The HC-SR04 continuously measures the distance in front of the robot.

If no obstacle is detected within the defined threshold, the robot continues moving forward.

When an obstacle is detected:

1. The robot stops.
2. It moves slightly backward.
3. The servo rotates the ultrasonic sensor to scan the left and right sides.
4. The measured distances are compared.
5. The robot turns toward the side with more free space.
6. The servo returns to the center position and the robot continues moving.

## Repository Structure

```text
pico2w-obstacle-avoiding-robot/
├── README.md
├── main.py
├── hardware-diagram.json
```

## Hardware Setup

### Components

- Raspberry Pi Pico 2 W
- L298N motor driver
- 2 × DC geared motors
- SG90 servo
- HC-SR04 ultrasonic sensor
- 2 × 2.2 kΩ resistors
- Breadboard
- Jumper wires
- 4 × AA battery pack
- Power switch
- USB power bank
- Robot chassis with wheels

### Pin Connections

| Component | Pin | Raspberry Pi Pico 2 W |
|---|---|---|
| Servo | Signal | GP0 |
| HC-SR04 | TRIG | GP2 |
| HC-SR04 | ECHO | GP3 through voltage divider |
| L298N | IN1 | GP5 |
| L298N | IN2 | GP6 |
| L298N | IN3 | GP7 |
| L298N | IN4 | GP8 |

### HC-SR04 Voltage Divider

The HC-SR04 ECHO output operates at 5 V, while the Raspberry Pi Pico GPIO pins use 3.3 V logic.

A voltage divider made from two 2.2 kΩ resistors is used:

ECHO → 2.2 kΩ → GP3 → 2.2 kΩ → GND

This reduces the ECHO voltage to approximately 2.5 V.

### Motor Driver

The L298N motor driver is configured with the ENA and ENB jumpers installed.

- GP4 and GP9 are not used.
- OUT1 / OUT2 → left motor
- OUT3 / OUT4 → right motor
- Pico GND → L298N GND

Motor wiring:

- Left motor: OUT1 → positive, OUT2 → negative
- Right motor: OUT4 → positive, OUT3 → negative

### Power

The robot uses two separate power sources:

- USB power bank → Raspberry Pi Pico 2 W via USB
- 4 × AA battery pack → power switch → L298N VIN
- Battery negative → L298N GND

The Raspberry Pi Pico 2 W and the L298N share a common ground.

If a USB power bank is not available, the Pico can instead be powered from the battery pack through a suitable DC-DC step-down (buck) converter providing a stable voltage within the Pico's supported input range.

A simple resistor voltage divider should not be used to power the Pico, because its output voltage changes with the load and is not suitable as a stable power source.

### Wiring Diagram
<img width="1046" height="994" alt="image" src="https://github.com/user-attachments/assets/6ef7e4cd-092f-4a77-abd7-f69402b6631a" />

The complete hardware layout is also included in the repository as hardware-diagram.json, which can be opened and edited in Wokwi.

## Software

The robot is programmed in MicroPython.

The main control logic is stored in `main.py`.

The software handles:

- ultrasonic distance measurement,
- servo-controlled scanning of the environment,
- forward and backward movement,
- left and right turns,
- obstacle detection,
- selection of the clearer direction when an obstacle is detected.

To run the robot, copy `main.py` to the Raspberry Pi Pico 2 W and save it on the board as `main.py`. The script will then start automatically when the Pico is powered.
