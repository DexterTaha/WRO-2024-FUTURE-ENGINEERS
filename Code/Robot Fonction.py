
# Register the standard input so we can read keyboard presses.
keyboard = poll()
keyboard.register(stdin)

# Initialize the hub, motors, and sensor
hub = InventorHub()
steer_motor = Motor(Port.D)
leftMotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
rightMotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftMotor, rightMotor, 56, 1 75)

# Tuning parameters
SPEED_MAX = 1000
SPEED_TURN = 500


def calibrate_steering():
    global steer_left_limit, steer_right_limit, steer_center

    # Find the Left limit
    steer_motor.run_until_stalled(
        -SPEED_TURN, then=Stop.BRAKE, duty_limit=60
    )
    steer_left_limit = steer_motor.angle()

    # Find the Right limit
    steer_motor.run_until_stalled(
        SPEED_TURN, then=Stop.BRAKE, duty_limit=60
    )
    steer_right_limit = steer_motor.angle()

    # Calculate the center as the average of the two limits
    steer_center = (steer_right_limit + steer_left_limit) // 2

    # Reset the angle to the center
    steer_motor.run_target(SPEED_TURN, steer_center, then=Stop.BRAKE, wait=False)

def affiche_data():
    # Print the values
    print("Left limit:", steer_left_limit)
    print("Right limit:", steer_right_limit)
    print("Center:", steer_center)

# Function to turn the steering wheel to the right limit
def turn_right():
    steer_motor.run_until_stalled(SPEED_TURN, then=Stop.BRAKE, duty_limit=60)

# Function to turn the steering wheel to the left limit
def turn_left():
    steer_motor.run_until_stalled(-SPEED_TURN, then=Stop.BRAKE, duty_limit=60)

def steer_to_center():
    # Run the motor to the calculated center angle
    steer_motor.run_target(SPEED_MAX, steer_center, then=Stop.BRAKE)
def move(speed):
    leftMotor.run(speed)
    rightMotor.run(speed)

def stop():
    leftMotor.stop()
    rightMotor.stop()

def main():
    # Call the calibration function
    calibrate_steering()
