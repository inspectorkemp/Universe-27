from machine import Pin, UART
import utime

# Define pin for the LED
LED_PIN = 25

# Define UART (MIDI)
uart = UART(0, baudrate=31250, tx=0, rx=1, txbuf=64, rxbuf=64)

# MIDI Note On and Note Off constants
NOTE_ON_STATUS = 0x90  # Note On status byte
NOTE_OFF_STATUS = 0x80  # Note Off status byte

# MIDI channel and note number for D#
MIDI_CHANNEL = 1
NOTE_D_SHARP = 63

def send_note_on(note, velocity):
    midi_message = bytes([NOTE_ON_STATUS | ((MIDI_CHANNEL - 1) & 0x0F), note, velocity])
    uart.write(midi_message)

def send_note_off(note):
    midi_message = bytes([NOTE_OFF_STATUS | ((MIDI_CHANNEL - 1) & 0x0F), note, 0])
    uart.write(midi_message)

# Setup LED pin
led = Pin(LED_PIN, Pin.OUT)

# Function to play a note and then stop with fading effect
def play_note_and_stop(note, duration):
    fade_duration = 1000  # Fading duration in milliseconds

    # Fading in
    for i in range(0, 256, 4):
        led.duty_u16(i * i)  # Squaring for a smoother fade
        send_note_on(note, i)
        utime.sleep_ms(fade_duration // 64)

    # Playing at full intensity
    led.duty_u16(65535)  # Full intensity
    send_note_on(note, 127)
    utime.sleep_ms(duration)

    # Fading out
    for i in range(255, -1, -4):
        led.duty_u16(i * i)
        send_note_on(note, i)
        utime.sleep_ms(fade_duration // 64)

    # Stopping the note
    send_note_off(note)
    led.duty_u16(0)  # Turn off the LED
    utime.sleep_ms(100)  # Optional: brief pause after stopping the note

# Main setup
def setup():
    led.off()
    uart.init(31250, tx=0, rx=1)
    
# Main loop
def loop():
    # Play D# (Note number 63) for 10 seconds with fading effect
    play_note_and_stop(NOTE_D_SHARP, 10000)

# Run setup
setup()

# Run loop
while True:
    loop()
