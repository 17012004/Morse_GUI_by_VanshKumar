import tkinter as tk
import RPi.GPIO as GPIO
import time
import threading

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

MorseCode = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': ' '
}

def Convert_to_Morse(text):
    return ' '.join([MorseCode.get(char.upper(), char) for char in text])

def Blink_Morse_Symbols(morse_text):
    for symbol in morse_text:
        if symbol == '.':
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.2)
        elif symbol == '-':
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.2)  # pause between symbols
        else:
            time.sleep(0.4)  # pause between words

def On_Convert_Button_Click():
    input_text = entry.get().strip()  # Strip leading/trailing spaces
    if len(input_text) > 12:
        error_label.config(text="Error: Characters exceed 12")
        return
    error_label.config(text="")
    morse_text = Convert_to_Morse(input_text)
    threading.Thread(target=Blink_Morse_Symbols, args=(morse_text,)).start()

# GUI settings
root = tk.Tk()
root.title("Morse Code Converter")

label = tk.Label(root, text="Enter text (max 12 characters):")
label.pack()

entry = tk.Entry(root)
entry.pack()

convert_button = tk.Button(root, text="Convert and Blink", command=On_Convert_Button_Click)
convert_button.pack()

# Add an error label to display error messages
error_label = tk.Label(root, text="Please enter 12 or less characters and not more than that", fg="red")
error_label.pack()

root.mainloop()

# Cleaning up the GPIO and resets its modes
GPIO.cleanup()
