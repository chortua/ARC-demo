import os
from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime
from azbil import status
import random
from api import *
import time
from Otto_kardex import *

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    print("Hello 1")
    try:
        #         Battery Set u
        b_level = get_vehicles(0)[0] # Get battery level for Nipper.
        state= get_vehicles(0)[2]
        nipperstate = get_vehicles(0)[1]
        #  Pallets status 
        now = datetime.now()
        current_time = now.strftime("%H:%M")
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

        #############>>>>>>     Nipper Buttons  set up.    <<<<<<<##########
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
                b_level = insert("nipper_grobal", "0-HP-Nipper")

            else:
                pass  # unknown
        elif request.method == 'GET':
            return render_template('index.html', b_level=b_level, nipperstate=nipperstate, state=state, color_main=color_main, color_d1=color_d1,
                               color_d2=color_d2, color_d3=color_d3)


        return render_template('index.html',  b_level=b_level, color_main=color_main, color_d1=color_d1,
                               color_d2=color_d2, color_d3=color_d3)



    except:
        message = 'Ant Server(Windows10 VM) or Nipper are not on。'
        message1 = '1) Windows10の仮想マシンに接続し、Antサーバーを起動してください。'
        nipper_ping = os.system("ping -c 1 192.168.128.65")
        if  nipper_ping == 0:
            message2 =  ' Nipper is ON (接続しました )'
        else:
            message2 =  'Nipper is off ( Can not localize Nipper ), Nipper をONにしてください.'
        message3 = message + 'Please insert Vehicle(挿入して) :'

        return render_template( "this.html", message=message, message1=message1, message2=message2, message3=message3 )



#############################################################    OTTO     #######################################################################


@app.route("/otto", methods=['GET','POST'])
def otto():

    try:

        bo_level = int(otto_battery()[1])  # Battery level for Otto 100
        bf_level = int(otto_battery()[0])  # Battery level for Otto 1500
        

        data = ""

        if request.method == 'POST':
            data = ""
            if request.form.get('ooneA1') == ('Pick up @ Kardex'):
                gotoMPX100()
            elif request.form.get('ooneA2') == ('Pick up @ MPX'):
                gotoKardex100()
            elif request.form.get('ooneB1') == ('充電する'):
                otto100parking()
            elif request.form.get('ooneB2') == ('Go To Parking'):
                otto100parking()
            elif request.form.get('ofifthA1') == ('Park @ Kardex'):
                ottokardex()
            else:
                pass  # unknown
        elif request.method == 'GET':
            return render_template('otto.html', data=data, bo_level=bo_level, bf_level=bf_level)


        return render_template('otto.html', bo_level=bo_level, bf_level=bf_level)
    except:
        return '<h1>hello from Otto</h1>'



######################## Kardex ###############################
@app.route("/kardexotto", methods=['GET','POST'])
def kardexotto():
    if request.method == 'POST':
        time.sleep(1)
        if request.form.get('kardex/otto') == 'Start Demo':
            move_cart(kardex_right, B_place)
            time.sleep(2)
            pull_out_tray(7)
            move_cart(B_place, kardex_right)
    else:
        render_template("kardexotto.html")
    return render_template("kardexotto.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) #port=80
