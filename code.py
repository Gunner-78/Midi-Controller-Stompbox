import board
import digitalio
import time
import usb_midi


# Create a MIDI out instance
midi_out = usb_midi.ports[1]

# Define button GPIO pins
button_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7]

# Initialize button objects
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]


# Set button direction to input
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Define MIDI note numbers for each button
note_numbers = [50, 51, 52, 53, 54, 55, 56, 57]

# Initialize previous button states for debounce
prev_button_states = [True] * 8


# Main loop
while True:
    # Read button states
    button_states = [not button.value for button in buttons]  # Invert because pull-up resistor is used

    # Check for button press and send MIDI messages
    for i in range(8):
        if button_states[i] != prev_button_states[i]:
            if button_states[i]:  # Button is pressed
                midi_out.write(bytearray([0x90, note_numbers[i], 120]))  # Note on
            else:  # Button is released
                midi_out.write(bytearray([0x80, note_numbers[i], 0]))  # Note off

    # Update previous button states
    prev_button_states = button_states

    # Add a small delay to debounce buttons
    time.sleep(0.01)
