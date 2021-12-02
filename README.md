# socket-mouse

## Instructions Serial Solution
### Install Touchcontrol (Serial)
The script **touchcontrol.py** has to be installed on the client (linux) and should be run by pm2 with python3.
The purpose of this script is to capture input events from the beamer hardware and recalculate the corresponding co-ordinates, filter ghost touches and send touch events to the micro controller (arduino) via serial.

## Instructions Socket Solution
### Install Touchcontrol (Socket)
The script **sc_tc.py** has to be installed on the client (linux) and should be run by pm2 with python3.
The purpose of this script is to capture input events from the beamer hardware and recalculate the corresponding co-ordinates, filter ghost touches and send touch events to the server (windows) via socket.

The scripts **ss_tc.py** or **ss_mc.py** has to be installed on server (windows) and should be run by pm2 with python3.
The purpose of this script is to receive the touch events from the client script **sc_tc.py**.

## Instructions Keycontrol
### Install Keycontrol
The script **keycontrol.py** has to be installed on server (windows) and can be run by pm2 with python3.

### -OR alternative -

## Instruction App Solution
### Install APP (alternativ for Socket/Serial Solution and Keycontrol)
The script **sc_tc.py** has to be installed on the client (linux) and should be run by pm2 with python3. The purpose of this script is to capture input events from the beamer hardware and recalculate the corresponding co-ordinates, filter ghost touches and send touch events to the server (windows) via socket.

The script **app.py** is a gui that also run to processes (keyctrl and touchctrl) to receive touch events and keyboard events. 
The purpose of this script is to provide a gui to change the bookmark for the key events and listen to them. It also receives the touch events from the **sc_tc.py** script send by the client (linux)


## PM2
### To see the process running in pm2
```
pm2 ls
```

### How to start if script is not running in pm2
```
pm2 start src/touchcontrol.py --name touchcontrol --restart-delay 3000 --time --interpreter python3
```
