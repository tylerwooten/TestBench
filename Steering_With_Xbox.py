import pygame
import can
from can import Message
import os
import time

# Set bitrate
os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')

# Set bus
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ------------------------------ START COMMAND ENCODER FUNCTION --------------------------------------- #
def command_encoder(position, speed):
    # example command to run: command_encoder(0.29, 0.6), 0.29 rev at 0.6 speed

    # IQ20 conversion
    convert_position = float(position * 2 ** 20)
    convert_speed = float(speed * 2 ** 8)

    # Initializing number of bits for each variable
    position_bits = 32
    speed_bits = 16

    # Conversion of position to hex
    hex_position = hex((int(convert_position) + (1 << position_bits)) % (1 << position_bits))
    while len(hex_position) < 10:
        hex_position = str(hex_position)
        hex_position = hex_position[:2] + '0' + hex_position[2:]

    # Conversion of speed to hex
    hex_speed = hex((int(convert_speed) + (1 << speed_bits)) % (1 << speed_bits))
    while len(hex_speed) < 6:
        hex_speed = str(hex_speed)
        hex_speed = hex_speed[:2] + '0' + hex_speed[2:]

    n = 2
    
    hex_position = (str(hex_position[2:]))
    holder_position = [hex_position[i:i + n] for i in range(0, len(hex_position), n)]

    hex_speed = (str(hex_speed[2:]))
    holder_speed = [hex_speed[i:i+n] for i in range(0, len(hex_speed), n)]

    command = holder_position[::-1] + holder_speed[::-1]

    test_command = ''.join(command)
    holder_command = [test_command[i:i + n] for i in range(0, len(test_command), n)]

    print(holder_command)

    final_command = []
    for item in holder_command:
        item = int(item, 16)
        final_command.append(item)

    temp_list = [5, 255]
    temp_list.extend(final_command)

    # Create message_send and return it to function caller
    message_send = Message(arbitration_id=419365113, data=temp_list)
    return message_send

# ------------------------------ START KAR TECH ENCODER FUNCTION --------------------------------------- #
def Kar_tech_encoder(position):
    # identifier is no longer needed. This is defined in the send bus message.
    # position in inches that the actuator should go to

    # initializing 8 byte container
    can_message = ['00', '00', '00', '00', '00', '00', '00', '00']
    # byte 0 and byte 1 will always be these values
    can_message[0] = '0f'
    can_message[1] = '4a'

    # position (inches) multiplied by 1000
    adjusted_position = position * 1000
    # offset defined by Kar Tech Actuator documentation
    offset = 500
    # Value that needs to be turned into hexadecimal
    adjusted_position_with_offset = adjusted_position + offset

    # Changing decimal to hex value
    hex_value = hex(int(adjusted_position_with_offset))
    # Removing '0x' from the start of the hex value
    hex_value_no_0x = hex_value[-3:]

    # Take last two of hex value and set to byte 2
    byte_2_hex = hex_value_no_0x[-2:]
    # Take first letter of hex value and set to byte 3
    byte_3_hex = 'c' + hex_value_no_0x[0]

    # Assigning bytes to the can message
    can_message[2] = byte_2_hex
    can_message[3] = byte_3_hex

    print('identifier: ', identifier)
    print('position: ', position)
    print('can message: ', can_message)

    # Initializing empty container
    send_message = [] # list of integers format -> [00, 00, 00, 00, 00, 00, 00, 00]
    # Looping through bytes in can message and turning into decimal
    for item in can_message:
        item = int(item, 16)
        send_message.append((item))

    message_send_actuator = Message(arbitration_id=16711680, data=send_message)
    return message_send_actuator


# ----------------------------------START XBOX CONTROLLER SECTION ---------------------------------------------- #


# Initializing pygame class "TextPrint".
# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)  # font description

    def printtext(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Drive By Wire")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop ----------- #
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # Draw number of joysticks
    textPrint.printtext(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.printtext(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printtext(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.printtext(screen, "Number of axes: {}".format(axes))  # draw number of axes
        textPrint.indent()

        # for each axis
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.printtext(screen, "Axis {} value: {:>6.3f}".format(i, axis))  # draw axis number and value
        textPrint.unindent()

        # Buttons section
        buttons = joystick.get_numbuttons()
        textPrint.printtext(screen, "Number of buttons: {}".format(buttons))  # draw number of buttons
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.printtext(screen, "Button {:>2} value: {}".format(i, button))  # draw button number and value
        textPrint.unindent()

        ################ ---------------- Joystick to Can Message --------------------- ######################
        axis0 = joystick.get_axis(0)  # Left knob, left (-1) and right (1)
        axis1 = joystick.get_axis(1)  # Left knob, up (-1) and down (1)
        axis2 = joystick.get_axis(2)  # Left Trigger, Left (1) Right (-1)
        axis5 = joystick.get_axis(5)  # Right Trigger, Left (1) Right (-1)
        button_A = joystick.get_button(0)  # A = button 0
        button_B = joystick.get_button(1)  # B = button 1
        button_X = joystick.get_button(2)  # X = button 2
        button_Y = joystick.get_button(3)  # Y = button 3

        # function to change -1 to 1 controller input into 0 to 3 inch stroke of actuator
        actuator_position = 1.5 * axis5 + 1.5

        speed = 1  # speed mode

        # if a button is held down, change the speed mode
        if button_A == 1:
            button_B = 0
            button_X = 0
            button_Y = 0
            speed = 0.1

        elif button_B == 1:
            button_X = 0
            button_A = 0
            button_Y = 0
            speed = 0.3

        elif button_X == 1:
            button_B = 0
            button_A = 0
            button_Y = 0
            speed = 0.7

        elif button_Y == 1:
            button_B = 0
            button_A = 0
            button_X = 0
            speed = 1

        else:
            speed = 1

        # TODO: recommend adding on a limit multiplier/divider of axis0 so we can expand or contract the max/min turn amount

        multiplier = 1  # is used to alter the position to send. i.e. joystick full right with multiplier 5, position = 5 rev
        position = axis0*multiplier  # axis0 max/min values = 1,-1 respectively. Units are revolutions

        # Encoding the position and speed
        message_send = command_encoder(position, speed)  # position coming from joystick movement, speed from button being pressed

        # Encoding the position
        message_send_actuator = Kar_tech_encoder(actuator_position)

        # TODO: Find out how to send 2 can messages at the same time without interfering with eachother
        # Sending the message to the motor
        bus.send(message_send)
        time.sleep(0.001)  #
        bus.send(message_send_actuator)

        # TODO: Draw on display the steering position and the acceleration/braking amount

    # Update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second, motor internally limited to 1 ms send speed
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang' on exit if running from IDLE.
pygame.quit()
