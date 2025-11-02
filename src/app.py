import os
import time

SIMULATE = os.environ.get("SIMULATE", "0") == "1"

HOLD_SECONDS = float(os.environ.get("HOLD_SECONDS", 5))
PIR_PIN = int(os.environ.get("PIR_PIN", 17))  # HC-SR501 OUT → GPIO17
LED_PIN = int(os.environ.get("LED_PIN", 18))  # LED → GPIO18

if not SIMULATE:
    # Real hardware
    from gpiozero import MotionSensor, LED
    from signal import pause
    from threading import Timer

    pir = MotionSensor(PIR_PIN)
    led = LED(LED_PIN)
    timer = None

    def extend_hold():
        global timer
        if timer:
            timer.cancel()
        timer = Timer(HOLD_SECONDS, led.off)
        timer.start()

    def on_motion():
        led.on()
        extend_hold()

    def on_no_motion():
        extend_hold()

    pir.when_motion = on_motion
    pir.when_no_motion = on_no_motion

    print(
        f"Motion LED armed on PIR GPIO{PIR_PIN} → LED GPIO{LED_PIN}. "
        f"Hold: {HOLD_SECONDS}s. Ctrl+C to exit."
    )
    pause()

else:
    # Simulation: no GPIO required
    print(
        f"[SIMULATION] Running without GPIO. "
        f"PIR_PIN={PIR_PIN}, LED_PIN={LED_PIN}, HOLD_SECONDS={HOLD_SECONDS}"
    )
    last_motion = 0
    led_on = False

    def motion_event():
        nonlocal led_on, last_motion  # type: ignore  # for Python <3.11 linters
        led_on = True
        last_motion = time.time()
        print("[SIM] Motion detected → LED ON")

    print("[SIM] Press Ctrl+C to stop. Simulating motion every 3 seconds...")
    try:
        while True:
            now = time.time()
            # pretend we detect motion every 3 seconds
            if int(now) % 3 == 0 and (now - last_motion) > 1.1:
                motion_event()

            # auto-off after HOLD_SECONDS
            if led_on and (now - last_motion) > HOLD_SECONDS:
                led_on = False
                print("[SIM] Quiet period elapsed → LED OFF")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[SIM] Exiting cleanly.")
