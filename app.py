import os
from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime
from azbil import status
import random
from api import *
import time


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    try:

        #         Battery Set u
        b_level = get_vehicles(0)[0] # Get battery level for Nipper.
        state= get_vehicles(0)[2]
        nipperstate = get_vehicles(0)[1]
        bm_level = random.randint(0,100) # battery level for MPX
        bo_level = 10  # Battery level for Otto 100
        bf_level = 15  # Battery level for Otto 1500
        brf_level = random.randint(0, 100)  # Battery level for Robofork

        #         Bottom set up.
        data = ""

        if request.method == 'POST':
            data = ""
            if request.form.get('nipperA1') == 'Pick up Cart':
                create_mission("0-PickupCart", "0-DropCart")
            elif request.form.get('nipperA2') == '抜き取る':
                extract("nipper_grobal")
            elif request.form.get("nipperB1") == "充電する":
                create_mission("0-StartPosition", "0-Nipper Charger")
            elif request.form.get("nipperB2") == "挿入する":
                # Inserting the vehicle, ( Vehicle name, node name )
                b_level = insert("nipper_grobal", "0-HP-Nipper")
            else:
                pass  # unknown
        elif request.method == 'GET':
            return render_template('index.html', data=data, b_level=b_level, bm_level=bm_level,
                               bo_level=bo_level, bf_level=bf_level, brf_level=brf_level, nipperstate=nipperstate, state=state)


        return render_template('index.html',  b_level=b_level, bm_level=bm_level,
                               bo_level=bo_level, bf_level=bf_level, brf_level=brf_level)
    except:
        
        message = '<h1 align=middle >Ant Server(Windows10 VM) or Nipper are not on。</h1> '
        message = message + '<p align=middle> 1) Windows10の仮想マシンに接続し、Antサーバーを起動してください。</p>'
        nipper_ping = os.system("ping -c 1 192.168.128.65")
        if  nipper_ping == 0:
            message = message + '<p align=middle> Nipper is ON (接続しました )</p>'
        else:
            message = message + '<p align=middle> 2) Nipper is off ( Can not localize Nipper ), Nipper をONにしてください.</p>'  
        message = message + '<p align=middle>Please insert Vehicle(挿入して) :<a href="http://192.168.128.123:8081/wms/monitor/index.html#login">Ant server link</a> '
        
        return message

@app.route("/nipper")
def nipper():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    main_pickup, drop1, drop2, drop3 = status()
    color_main = "background-color:#b4d6db;"
    color_d1 = "background-color:#b4d6db;"
    color_d2 = "background-color:#b4d6db;"
    color_d3 = "background-color:#b4d6db;"
    if main_pickup == 1:
        color_main = "background-color:red;"
    if drop1 == 1:
        color_d1 = "background-color:red;"
    if drop2 == 1:
        color_d2 = "background-color:red;"
    if drop3 == 1:
        color_d3 = "background-color:red;"
    return render_template('nipper.html', current_time=current_time, color_main=color_main, color_d1=color_d1,
                               color_d2=color_d2, color_d3=color_d3)


@app.route("/demo")
def demo():
    return render_template("demo.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
