from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us

# Servo
servo = PWM(Pin(0))
servo.freq(50)

def set_servo(angle):
    min_us = 600
    max_us = 2400

    pulse = min_us + (angle / 180) * (max_us - min_us)
    duty = int(pulse / 20000 * 65535)

    servo.duty_u16(duty)

# HC-SR04, TRIG: GP2, ECHO: GP3 through 2.2k / 2.2k voltage divider

TRIG = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)


def distance_cm():
    # Minimum delay between ultrasonic measurements
    sleep_us(60000)

    TRIG.value(0)
    sleep_us(5)

    TRIG.value(1)
    sleep_us(10)
    TRIG.value(0)

    duration = time_pulse_us(ECHO, 1, 40000)

    if duration < 0:
        return None

    distance = duration * 0.0343 / 2

    if distance < 2 or distance > 400:
        return None

    return distance


def get_distance():
    # Try up to three times
    for _ in range(3):
        distance = distance_cm()

        if distance is not None:
            return distance

        sleep(0.05)

    return None


def measure_direction(angle):
    set_servo(angle)
    sleep(0.7)

    measurements = []

    for _ in range(3):
        distance = get_distance()

        if distance is not None:
            measurements.append(distance)

        sleep(0.08)

    if not measurements:
        return 0

    return sum(measurements) / len(measurements)


# L298N MOTOR DRIVER: GP5 -> IN1, GP6 -> IN2, GP7 -> IN3, GP8 -> IN4

# RIGHT MOTOR:
# OUT1 -> +
# OUT2 -> -
# LEFT MOTOR:
# OUT4 -> +
# OUT3 -> -

IN1 = Pin(5, Pin.OUT)
IN2 = Pin(6, Pin.OUT)

IN3 = Pin(7, Pin.OUT)
IN4 = Pin(8, Pin.OUT)


def forward():
    # RIGHT MOTOR forward
    IN1.value(1)
    IN2.value(0)

    # LEFT MOTOR forward
    IN3.value(0)
    IN4.value(1)


def backward():
    # RIGHT MOTOR backward
    IN1.value(0)
    IN2.value(1)

    # LEFT MOTOR backward
    IN3.value(1)
    IN4.value(0)


def turn_left():
    # RIGHT MOTOR forward
    IN1.value(1)
    IN2.value(0)

    # LEFT MOTOR backward
    IN3.value(1)
    IN4.value(0)


def turn_right():
    # RIGHT MOTOR backward
    IN1.value(0)
    IN2.value(1)

    # LEFT MOTOR forward
    IN3.value(0)
    IN4.value(1)


def stop():
    IN1.value(0)
    IN2.value(0)

    IN3.value(0)
    IN4.value(0)

CENTER = 90
LEFT_ANGLE = 140
RIGHT_ANGLE = 50

STOP_DISTANCE = 20

BACK_TIME = 0.25
TURN_TIME = 0.35

stop()

set_servo(CENTER)
sleep(1)


# main loop

while True:

    front_distance = get_distance()

    # No valid ultrasonic reading
    if front_distance is None:
        print("No echo")

        stop()
        sleep(0.2)

        continue

    print("Front:", round(front_distance, 1), "cm")

    if front_distance > STOP_DISTANCE:
        forward()

    # obstacle detected

    else:
        print("OBSTACLE")

        stop()
        sleep(0.3)

        # Move slightly backward
        backward()
        sleep(BACK_TIME)

        stop()
        sleep(0.3)

        # Look left
        left_distance = measure_direction(LEFT_ANGLE)

        print(
            "Left:",
            round(left_distance, 1),
            "cm"
        )

        # Look right
        right_distance = measure_direction(RIGHT_ANGLE)

        print(
            "Right:",
            round(right_distance, 1),
            "cm"
        )

        # Return sensor to center
        set_servo(CENTER)
        sleep(0.5)

        # Choose clearer direction
        if left_distance > right_distance:

            print("TURN LEFT")

            turn_left()
            sleep(TURN_TIME)

        else:

            print("TURN RIGHT")

            turn_right()
            sleep(TURN_TIME)

        stop()
        sleep(0.25)
