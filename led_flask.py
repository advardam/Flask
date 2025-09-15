from flask import Flask, render_template, redirect, url_for
from gpiozero import LED
from gpiozero.pins.lgpio import LGPIOFactory
import time
import threading
import atexit

# Use LGPIOFactory explicitly for safe pin handling
pin_factory = LGPIOFactory()

# Define LEDs (BCM pins)
led1 = LED(17, pin_factory=pin_factory)
led2 = LED(27, pin_factory=pin_factory)

app = Flask(__name__)

# Flag to control blinking thread
blinking = False
blink_thread = None


def blink_leds():
    """Blink both LEDs together until stopped."""
    global blinking
    while blinking:
        led1.on()
        led2.on()
        time.sleep(0.5)
        led1.off()
        led2.off()
        time.sleep(0.5)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/on")
def led_on():
    global blinking
    blinking = False
    led1.on()
    led2.on()
    return redirect(url_for("index"))


@app.route("/off")
def led_off():
    global blinking
    blinking = False
    led1.off()
    led2.off()
    return redirect(url_for("index"))


@app.route("/blink")
def start_blink():
    global blinking, blink_thread
    if not blinking:
        blinking = True
        blink_thread = threading.Thread(target=blink_leds)
        blink_thread.start()
    return redirect(url_for("index"))


@app.route("/stop")
def stop_blink():
    global blinking
    blinking = False
    return redirect(url_for("index"))


# Cleanup GPIO on exit
atexit.register(lambda: (led1.close(), led2.close()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
