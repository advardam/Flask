from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO setup
LED1 = 17
LED2 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

# Store LED states
led_states = {LED1: False, LED2: False}

@app.route("/")
def index():
    return render_template(
        "index.html",
        led1=led_states[LED1],
        led2=led_states[LED2]
    )

@app.route("/<led>/<action>")
def led_action(led, action):
    if led == "led1":
        pins = [LED1]
    elif led == "led2":
        pins = [LED2]
    elif led == "both":  # 🔥 New case for both LEDs
        pins = [LED1, LED2]
    else:
        return redirect(url_for("index"))

    if action == "on":
        for pin in pins:
            GPIO.output(pin, GPIO.HIGH)
            led_states[pin] = True
    elif action == "off":
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)
            led_states[pin] = False
    elif action == "blink":
        for i in range(5):  # blink 5 times
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)
        for pin in pins:
            led_states[pin] = False  # After blinking, set OFF

    return redirect(url_for("index"))

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
