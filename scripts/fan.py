#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys

TX_PIN = 18
PULSE_LENGTH = 0.0004*0.85
DELAY_AFTER_PREAMBLE = 0.005
DELAY_AFTER_COMMAND = 0.025
DELAY_BETWEEN_DOUBLE_COMMAND = 0.285
PREAMBLE =  "101010101010101010101010"
COMMAND_PREFIX = "01000101111001100110101111010000111110010111"

COMMANDS = {
  "light": [
    "0111111110001000000001",
    "1110110010000001001101"
  ],
  "fan_off": [
    "1111111100000000000010",
    "1110111010000001000100"
  ],
  "fan1": ["1111111010000000000100"],
  "fan2": ["1110111110000001000001"],
  "fan3": ["1101111110000010000001"]
}

def send_value(value):
  GPIO.output(TX_PIN, value)
  time.sleep(PULSE_LENGTH)

def send_0():
  send_value(GPIO.HIGH)
  send_value(GPIO.HIGH)

def send_1():
  send_value(GPIO.HIGH)
  send_value(GPIO.LOW)

def send_separator():
  send_value(GPIO.LOW)

def send_command_part(part):
  for bit in PREAMBLE:
    if bit == "1":
      GPIO.output(TX_PIN, GPIO.HIGH)
      time.sleep(PULSE_LENGTH)
    elif bit == "0":
      GPIO.output(TX_PIN, GPIO.LOW)
      time.sleep(PULSE_LENGTH)

  GPIO.output(TX_PIN, GPIO.LOW)
  time.sleep(DELAY_AFTER_PREAMBLE)

  rest = COMMAND_PREFIX + part
  for bit in rest:
    if bit == "0":
      send_0()
    elif bit == "1":
      send_1()
    send_separator()
  time.sleep(DELAY_AFTER_COMMAND)


if __name__ == "__main__":
  # Pin Setup:
  GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
  GPIO.setup(TX_PIN, GPIO.OUT)
  try:
    choice = sys.argv[1]
    for part in COMMANDS[choice]:
      send_command_part(part)
      send_command_part(part)
  finally:
    GPIO.cleanup() # cleanup all GPIO
