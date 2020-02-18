from losantmqtt import Device
import datetime
import json
import time
import os

import chargeController
import currentMonitor
import relayBox
import database
import sensors


data = dict()

ACCESS_KEY = 'eed2fd5b-8219-4b18-a858-cdf345185cd6'
ACCESS_SECRET = '1d8c634d39551e13a6da838bfdc152cdc43e10362bca3a888cbfc2a411020dd3'
DEVICE_ID = '5e2ec7308eb4af0006ecd530'

DELAY = 1.0


def sendDataToLosant(data):

    print("Sending to Losant...")
    device.send_state(data)


def connectToLosant():

    # Connect to Losant and leave the connection open
    global device
    device.connect(blocking=False)


def to_tuple(data):
    ret = (
        data['panelVoltage'],
        data['panelCurrent'],
        data['batteryVoltage'],
        data['batteryCurrent'],
        data['loadVoltage'],
        data['loadCurrent'],
        data['inPower'],
        data['outPower'],   
        data['plug_1_current'],
        data['plug_2_current'],  
        data['inverter_current'],
        data['irradiation']
    )
    return ret


def init():

    database.init()


def on_command(device, command):

    print(command["name"] + " command received")
    print(command["state"])

    # if command["name"] == relayBox.PLUG_A_ID:

    #     if command["state"] == "ON":
    #         relayBox.enablePlugA()
    #     else:
    #         relayBox.disablePlugA()
    

    # elif command["name"] == relayBox.PLUG_B_ID:

    #     if command["state"] == "ON":
    #         relayBox.enablePlugB()
    #     else:
    #         relayBox.disablePlugB()
    

    # elif command["name"] == relayBox.INVERTER_ID:

    #     if command["state"] == "ON":
    #         relayBox.enableInverter()
    #     else:
    #         relayBox.disableInverter()
    

    # elif command["name"] == relayBox.EXTERNAL_SOURCE_ID:

    #     if command["state"] == "ON":
    #         relayBox.enableExternalPower()
    #     else:
    #         relayBox.disableExternalPower()


# Construct Losant device
device = Device(DEVICE_ID, ACCESS_KEY, ACCESS_SECRET)
device.add_event_observer("command", on_command)


def main():

    print('Gionji Solar Plant')
    
    connectToLosant()

    currentMonitor.calculateCurrentBias(currentMonitor.PLUG_1)
    currentMonitor.calculateCurrentBias(currentMonitor.PLUG_2)
    currentMonitor.calculateCurrentBias(currentMonitor.INVERTER)
    
    # Initialize the database. This amounts to creating a table if it doesn't exist
    database.init()

    while True:

        global data
        data = dict()

        # Read all the data provided by the Charge Controller
        data = chargeController.readAll()

        try:

            # Read irradiation data
            data['irradiation'] = sensors.getIrradiation()

        except Exception as e:

            data['irradiation'] = None 
            print(e)

        try:

            # Read current-related data
            data['plug_1_current'] = currentMonitor.getCurrentPlug1()
            data['plug_2_current'] = currentMonitor.getCurrentPlug2()
            data['inverter_current'] = currentMonitor.getCurrentInverter()    
        
        except Exception as e:

            data['plug_1_current'] = None
            data['plug_2_current'] = None
            data['inverter_current'] = None
            print(e)

        try:
            # Send data to Losant
            sendDataToLosant(data)

        except Exception as e:
            print(e)

        # Pack data to db. In order to be able to insert it into the table, data must be formatted as a tuple
        data = to_tuple(data)

        # Print data
        # print(data)

        # Insert data into db
        database.insert_data(data)
        
        ## select all data
        #database.select_data_all()

        time.sleep(DELAY)


if __name__ == "__main__":
    main()