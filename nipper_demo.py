from azbil import *
from ANTServerMain import *
import time

while True:
    time.sleep(5)
    if status()[0] == 1 and status()[1] == 0 :
        time.sleep(0.25)
        print("Waiting for 25mseconds parking 1")
        if status()[0] == 1 and status()[1] == 0:
            print("Parking 1 Mission created")
            create_mission_and_confirmation("0-Nipper Main PickUp", "0-Nipper Drop_1", " Going to drop at parking 1")
    elif status()[0] == 1 and status()[2] == 0:
        time.sleep(0.25)
        print("Waiting for 25mseconds parking 2")
        if status()[0] == 1 and status()[2] == 0:
            print("Parking 2 Mission created")
            create_mission_and_confirmation("0-Nipper Main PickUp", "0-Nipper Drop_2", " Going to drop at parking 2")
    elif status()[0] == 1 and status()[3] == 0:
        print("Waiting for 25mseconds parking 3")
        time.sleep(0.25)
        if status()[0] == 1 and status()[3] == 0:
            print(" Parking 3 Mission created")
            create_mission_and_confirmation("0-Nipper Main PickUp", "0-Nipper Drop_3", " Going to drop at parking 3")
    else:
        print("On Stand by")
        


