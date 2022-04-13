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
    o_battery = []
    o_battery.append((token_data['results'][0]['percentage']) * 100)  # OTTO 1500
    o_battery.append((token_data['results'][1]['percentage']) * 100)  # OTTO 100
    return( o_battery)

kardex_right = "f93ba577-75c8-4d13-9a4d-94b0bbc96857"
kardex_left = "76db5835-bf5a-4cd0-b14d-b838bd8f23eb"
A_place = "ea4cb1cb-a22b-4215-9973-61fd69167737"
B_place = "e2261cb9-ca8d-4791-9bcd-b206708f435d" # not being used 100
C_place = "a91dc8c2-f104-48d5-b107-faa72f5dd7aa" # not being used 100
parking2_pl = "703e61e3-f86a-4ef5-8b58-47f581358059" # # not being used 100
Supply_pl = "c9031fbe-50f0-440c-a567-a620ee91b2ee" # not being used
parkingbykardexid = "8785e6e3-4137-4d8e-927c-9e6fe49276c5"
parkingshowid = "e3788992-894d-4b6b-baf1-1757df360c16"
parking_wp_place = "bc3a9ae2-78ff-48a3-afb0-e83164961349" # use this with keypad

ottoserver = "https://192.168.128.40"

kardextoA = {
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
        "place": kardex_right,
        "task_type": "MOVE"
      },
      {
        "description": "Pickup red cart",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": kardex_right,
        "task_type": "LOAD"
      },
      {
        "description": "Transport cart to point A",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": A_place,
        "task_type": "TRANSPORT"
      },
      {
        "description": "Drop the red card at point A",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": A_place,
        "task_type": "UNLOAD"
      },
    ]
  }
}
Atokardex = {

  "id": 11112,
  "jsonrpc": "2.0",
  "method": "createMission",
  "params": {
    "mission": {
      "description": "More Red cart from point A to kardex",
      "finalized": "true"
    },
    "tasks": [
      {
        "description": "Move to point A",
        "place": A_place,
        "task_type": "MOVE"
      },
      {
        "description": "Pickup a payload",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": A_place,
        "task_type": "LOAD"
      },
      {
        "description": "Move red cart to kardex",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": kardex_right,
        "task_type": "TRANSPORT"
      },
      {
        "description": "Drop off red cart at kardex",
        "payload": "64f6677e-d971-4aed-9a1f-994fd4f74d58",
        "place": kardex_right,
        "task_type": "UNLOAD"
      },
    ]
  }
}
parking = {
  "id": 11113,
  "jsonrpc": "2.0",
  "method": "createMission",
  "params": {
    "mission": {
      "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
      "description": "Going to general OTTO 100 parking",
      "finalized": "true"

    },
    "tasks": [
      {
        "description": "Example of a description for a task",
        "place": parking_wp_place,
        "task_type": "MOVE"
      }
    ]
  }
}

# otto 100 parking
parkingShow = {
  "id": 11114,
  "jsonrpc": "2.0",
  "method": "createMission",
  "params": {
    "mission": {
      "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
      "description": "Going to Parking show",
      "finalized": "true"

    },
    "tasks": [
      {
        "description": "Example of a description for a task",
        "place": parkingshowid,
        "task_type": "MOVE"
      }
    ]
  }
}
parkingbykardex = {
  "id": 11114,
  "jsonrpc": "2.0",
  "method": "createMission",
  "params": {
    "mission": {
      "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
      "description": "Going to Parking show",
      "finalized": "true"

    },
    "tasks": [
      {
        "description": "Example of a description for a task",
        "place": parkingbykardexid,
        "task_type": "MOVE"
      }
    ]
  }
}



def gotoMPX100():
    requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=kardextoA, verify=False)

def gotoKardex100():
    requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=Atokardex, verify=False)

def ottoparkingshow100():
  requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=parkingShow, verify=False)

def otto100parkingbykardex():
  requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=parkingbykardex, verify=False)

def otto100parking():
  requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=parking, verify=False)

# OTTO 1500 parking at Kardex
def ottokardex():
    payload2 = {
      "id": 11112,
      "jsonrpc": "2.0",
      "method": "createMission",
      "params": {
        "mission": {
          "client_reference_id": "1e68acc2-0742-4f33-ae2d-4d6964188a4d",
          "description": "1500- Going to Kardex ",
          "finalized": "true"
        },
        "tasks": [
          {
            "description": "Example of a description for a task",
            "place": wp1_1500,
            "task_type": "MOVE"
          }
        ]
      }
    }
    requests.post("https://192.168.128.40/api/fleet/v2/operations/post", json=payload2, verify=False)

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

