import requests
import warnings
import time

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
ipport = "http://192.168.128.123:8081"
def otto_battery():
    # here is the battery level on OTTO's unit
    response_battery = requests.get(url="https://192.168.128.40/api/fleet/v2/robots/batteries/?fields=percentage,robot&limit=100&ordering=id", verify=False)
    response_battery.raise_for_status()
    token_data = response_battery.json()
    o_battery0 = (token_data['results'][0]['percentage'])  # OTTO 1500
    o_battery1 = (token_data['results'][1]['percentage'])  # OTTO 100
    return( o_battery0, o_battery1)

def ottostart():
    payload = {
        "id": 11111,
        "jsonrpc": "2.0",
        "method": "createMission",
        "params": {
            "mission": {
                "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
                "description": "Start Point",
                "finalized": "true"

            },
            "tasks": [
                {
                    "description": "Example of a description for a task",
                    "place": "4e5355cf-fbc4-4c86-9517-bcb66cdc5d25",
                    "task_type": "MOVE"
                }
            ]
        }
    }
    p1 = requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=payload, verify=False)
    print(p1.text)


def ottowp1():
    payload2 = {
        "id": 11112,
        "jsonrpc": "2.0",
        "method": "createMission",
        "params": {
            "mission": {
                "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
                "description": "Going to parking 1",
                "finalized": "true"

            },
            "tasks": [
                {
                    "description": "Example of a description for a task",
                    "place": "86bf0396-79f8-441a-abf0-2d61abbb4956",
                    "task_type": "MOVE"
                }
            ]
        }
    }
    p2 = requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=payload2, verify=False)
    print(p2.text)


def ottostatus():
    response_status = requests.get(
        url="https://192.168.128.40/api/fleet/v2/missions/?fields=id&limit=1&mission_status=SUCCEEDED",
        verify=False)
    response_status.raise_for_status()

    rowdata_status = response_status.json()

    return rowdata_status["count"]


def ottoready():
    reference = ottostatus() + 1
    while True:

        if ottostatus() == reference:
            print(ottostatus(), reference)
            return True
        
        
        
################################# BlueBotics ######################################
################################# BlueBotics ######################################
################################# BlueBotics ######################################


################################## GET TOKEN ########################################
def gettoken():
    response = requests.get(url= ipport + "/wms/monitor/session/login?username=admin&pwd=123456")
    response.raise_for_status()
    rowdata = response.json()
    #print(rowdata["payload"]["sessiontoken"])
    return rowdata["payload"]["sessiontoken"]


#################################  INSERT ########################################
def insert(avg, node):
    tokenr = gettoken()
    insert_url = ipport + "/wms/rest/vehicles/"+ avg +"/command?&sessiontoken=" + tokenr
    homeposition = {
        "command": {
            "name": "insert",
            "args": {
                "nodeId": node
            }
        }
    }

    response = requests.post(insert_url, json=homeposition)
    response.raise_for_status()
    rowdata = response.json()
    return int(rowdata["payload"]["vehicle"]["state"]["battery.info"][0])

def extract(avg):
    tokenr = gettoken()
    extract_url = ipport + "/wms/rest/vehicles/" + avg + "/command?&sessiontoken=" + tokenr

    extraction = {
     "command": {
        "name": "extract",
        "args": {}
        }
    }
    response = requests.post(extract_url, json=extraction)
    return response
################################ GET MISSIONS ########################################

def get_missions():
    tokenr = gettoken()
    response = requests.get(url=ipport + "/wms/rest/missions?&sessiontoken=" + tokenr)
    response.raise_for_status()
    rowdata = response.json()
    print(rowdata["payload"]["missions"][-1])
    return

################################ GET VEHICLES (Battery level) ###########################
def get_vehicles(avg):
    try:
        tokenr = gettoken()
        response = requests.get(url=ipport +"/wms/rest/vehicles?&sessiontoken=" + tokenr)
        response.raise_for_status()
        rowdata = response.json()
        bat = int(rowdata["payload"]["vehicles"][avg]["state"]["battery.info"][0])
        state = rowdata["payload"]["vehicles"][avg]["state"]["vehicle.state"][0]
        operatingstate = int(rowdata["payload"]["vehicles"][avg]["operatingstate"])

        return bat, operatingstate, state
    except KeyError:
        pass

################################ GO TO ANGLE ######################################
def create_mission(fromN, toN, comment="going somewhere"):
    tokenr = gettoken()
    pickaddress =   ipport + "/wms/rest/missions?&sessiontoken=" + tokenr
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
############################## CreateAMission ####################################
def create_mission_and_confirmation(fromN, toN, comment="Going somewhere"):
    nav_state = create_mission(fromN, toN, comment)
    mission_info(nav_state)
    return True

def mission_info(id):
    """ Requires the id of the mission. Will get the state of a mission, Navigation State 0 = Received, 1 = Accepted, 2 = Rejected, 3 = Started
    4 = Terminated, 5 = Cancelled"""
    time.sleep(1)
    tokenr = gettoken()
    total_url_address = ipport + "/wms/rest/missions/" + id + "?&sessiontoken=" + tokenr
    response = requests.get(url=total_url_address)
    response.raise_for_status()
    token_data = response.json()
    mission_status = token_data["payload"]["missions"][0]["navigationstate"]
    try:
        while mission_status != 4:
            mission_status = token_data["payload"]["missions"][0]["navigationstate"]
    except:
        print("Error found at Mission information")

    return mission_status

###############################
############################### PICK OTTO #########################################

def pickupotto():
    tokenr = gettoken()
    pickaddress = " http://localhost:8081/wms/rest/missions?&sessiontoken=" + tokenr
    pickotto = {
        "missionrequest": {
            "requestor": "jean",
            "missiontype": "7",
            "fromnode": "Pickup Otto",
            "tonode": "angle",
            "cardinality": "1",
            "priority": 2,
            "parameters": {
                "value": {
                    "payload": "Picking_from_OTTO"
                },
                "desc": "Mission extension",
                "type": "org.json.JSONObject",
                "name": "parameters"
            }
        }
    }
    p1 = requests.post(pickaddress, json=pickotto)
    print(p1)


################################ DROP OTTO ###################################

def dropotto():
    tokenr = gettoken()
    pickaddress = " http://localhost:8081/wms/rest/missions?&sessiontoken=" + tokenr
    drop_otto = {
        "missionrequest": {
            "requestor": "jean",
            "missiontype": "7",
            "fromnode": "DROP",
            "tonode": "angle",
            "cardinality": "1",
            "priority": 2,
            "parameters": {
                "value": {
                    "payload": "Dropping_on_OTTO"
                },
                "desc": "Mission extension",
                "type": "org.json.JSONObject",
                "name": "parameters"
            }
        }
    }
    p1 = requests.post(pickaddress, json=drop_otto)
    print(p1)


def getvehicle():
    try:
        tokenr = gettoken()
        address = ipport + "/wms/rest/vehicles?&sessiontoken=" + tokenr
        response = requests.get(url=address)
        response.raise_for_status()

        getmdata = response.json()
        payload = getmdata["payload"]["vehicles"][1]["location"]["currentnode"]["name"]

        return payload
    except KeyError:
        pass


def roboready():
    b = "something"
    while b != True:
        if getvehicle() == None:
            continue
        a = getvehicle()
        if b == a:
            continue
        if b != a and a == "angle" and b == "CD":
            b = True
            return True
        else:
            b = a

