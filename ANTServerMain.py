import requests
import time

ip_address = "192.168.128.123"
port = "8081"


def gettoken():
    ip_address = "192.168.128.123:8081"
    response = requests.get(
        url="http://" + ip_address + "/wms/monitor/session/login?username=admin&pwd=123456")
    response.raise_for_status()
    token_data = response.json()
    return ip_address, token_data["payload"]["sessiontoken"]



def create_mission(fromN, toN, comment="going somewhere"):
    ip, token = gettoken()
    pickaddress = " http://" + ip + "/wms/rest/missions?&sessiontoken=" + token
    to_angle = {
        "missionrequest": {
            "requestor": "Chris H",
            "missiontype": "7",
            "fromnode": fromN,
            "tonode": toN,
            "cardinality": "1",
            "priority": 2,
            "parameters": {
                "value": {
                    "payload": comment
                },
                "desc": "Mission extension",
                "type": "org.json.JSONObject",
                "name": "parameters"
            }
        }
    }

    response = requests.post(pickaddress, json=to_angle)
    response.raise_for_status()
    token_data = response.json()
    return token_data["payload"]['acceptedmissions'][-1]



def insertVehicle(avg, node):
    """It requires the vehicle name and the node it should be insterted"""
    print(" ----------- Inserting Vehicle ----------- ")
    ip, token = gettoken()
    insert_url = "http://" + ip + "/wms/rest/vehicles/" + avg + "/command?&sessiontoken=" + token
    hp = {
        "command": {
            "name": "insert",
            "args": {
                "nodeId": node
            }
        }
    }
    return requests.post(insert_url, json=hp)



def get_avg_info(name):
    """ Requires the name of the vehicle, it will return the location of the vehicle"""
    ip, token = gettoken()
    response = requests.get(url="http://" + ip + "/wms/rest/vehicles?&sessiontoken=" + token)
    response.raise_for_status()
    token_data = response.json()
    try:
        nodeid = token_data["payload"]["vehicles"]
        for i in nodeid:
            if (i["name"]) == name:
                return (i["location"]["currentnode"]["name"])
    except KeyError:
        pass



def create_mission_and_confirmation(fromN, toN, comment):
    nav_state = create_mission(fromN, toN, comment)
    mission_info(nav_state)
    return True



def mission_info(id):
    """ Requires the id of the mission. Will get the state of a mission, Navigation State 0 = Received, 1 = Accepted, 2 = Rejected, 3 = Started
    4 = Terminated, 5 = Cancelled"""
    time.sleep(1)
    ip, token = gettoken()
    total_url_address = "http://" + ip + "/wms/rest/missions/" + id + "?&sessiontoken=" + token
    response = requests.get(url=total_url_address)
    response.raise_for_status()
    token_data = response.json()
    mission_status = token_data["payload"]["missions"][0]["navigationstate"]
    try:
        while mission_status != 4:
            time.sleep(2)
            ip, token = gettoken()
            total_url_address = "http://" + ip + "/wms/rest/missions/" + id + "?&sessiontoken=" + token
            response = requests.get(url=total_url_address)
            response.raise_for_status()
            token_data = response.json()
            mission_status = token_data["payload"]["missions"][0]["navigationstate"]
    except:
        print("Error found at Mission information")

    return mission_status



def allowedtocross(avg, node):
    """ give the vehicle name , and the node you want the vehicle to send the signal ( allow other car to move )"""

    while True:

        if get_avg_info(avg) == node:
            print(avg, get_avg_info(avg), node)
            return True

        else:
            continue

