import RPi.GPIO as GPIO

def status():
    """ Status will  give you the status of four relays, normal state is 1, if they are triggered is 0.  pins used 12,16,18,22
        outputs are mp (main parking), p1 ( parking 1), p2 ( parking 2 ), p3 ( parking 3)
    """
    main_parking = 12
    parking_1 = 16
    parking_2 = 18
    parking_3 = 22
    # Insert the pins as input ( # 12,16,18,22 )
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(main_parking, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(parking_1, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(parking_2, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(parking_3, GPIO.IN, GPIO.PUD_DOWN)
    try:
        mp = GPIO.input(main_parking)
        p1 = GPIO.input(parking_1)
        p2 = GPIO.input(parking_2)
        p3 = GPIO.input(parking_3)
        return mp, p1, p2, p3
    finally:
        GPIO.cleanup()


