import requests
import time
import warnings
import subprocess

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

kardex_right = "f93ba577-75c8-4d13-9a4d-94b0bbc96857"  # Not used at the moment
kardex_left = "76db5835-bf5a-4cd0-b14d-b838bd8f23eb"
A_place = "ea4cb1cb-a22b-4215-9973-61fd69167737"
B_place = "e2261cb9-ca8d-4791-9bcd-b206708f435d"  # Table ( will park very close to the table )
C_place = "a91dc8c2-f104-48d5-b107-faa72f5dd7aa"  # not being used 100
parking2_pl = "703e61e3-f86a-4ef5-8b58-47f581358059"  # # not being used 100
Supply_pl = "c9031fbe-50f0-440c-a567-a620ee91b2ee"  # not being used
parkingbykardexid = "8785e6e3-4137-4d8e-927c-9e6fe49276c5"
parkingshowid = "e3788992-894d-4b6b-baf1-1757df360c16"
parking_wp_place = "bc3a9ae2-78ff-48a3-afb0-e83164961349"  # use this with keypad

ottoserver = "https://192.168.128.40"


def move_cart(fr_where, to_where):
    information = {
        "id": 11111,
        "jsonrpc": "2.0",
        "method": "createMission",
        "params": {
            "mission": {
                "description": "OTTO > kardex > pointA > kardex > parking.",
                "finalized": "true"
            },
            "tasks": [
                {
                    "description": "Move to Kardex loading section",
                    "place": fr_where,
                    "task_type": "MOVE"
                },
                {
                    "description": "Pickup red cart",
                    "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
                    "place": fr_where,
                    "task_type": "LOAD"
                },
                {
                    "description": "Transport cart to point A",
                    "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
                    "place": to_where,
                    "task_type": "TRANSPORT"
                },
                {
                    "description": "Drop the red card at point A",
                    "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
                    "place": to_where,
                    "task_type": "UNLOAD"
                },
            ]
        }
    }
    requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=information, verify=False)

def pull_out_tray(tray_number):
    cmd_open = "sudo mount.cifs -o password="" //192.168.128.123/fromHostToJmif /home/pi/fromHosttoJmif"
    subprocess.Popen(cmd_open, shell=True)
    time.sleep(3)
    """
        User will provide the tray number, Kardex will bring the tray leave it out for a few second, then
        will storage the tray.
    """
    data_file = open("/home/pi/fromHosttoJmif/data.txt", "w")
    data_file.write(
        f"0|4711|S01-1|00{tray_number}|00{tray_number}|10|4|99|Order|Part|Description|1098|432|0|1000|1200|CIS Text")
    data_file.close()
    print("command to bring tray has been created")
    time.sleep(30)
    # It will wait for 30 second and then return the tray
    data_file = open("/home/pi/fromHosttoJmif/data.txt", "w")
    data_file.write("0|4719|S01-1|0|0|0|0|0||||0|0|0|0|0|")
    data_file.close()
    print("Command to return the tray has been created")
    
    
#move_cart(kardex_right, B_place)
#time.sleep(2)
#pull_out_tray(7)
#move_cart(B_place, kardex_right)
