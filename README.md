# Bluetooth Flooder for Unihiker DFRobot card
This is a simple Bluetooth Flooder program designed for Unihiker DFRobot card. The program can scan for nearby Bluetooth devices using either Classic Bluetooth or BLE protocol, and send multiple ping requests to these devices to test their responsiveness. The number of ping requests can be specified by the user.

## Getting Started
### Prerequisites
Bleak library for scanning Bluetooth devices using BLE protocol
### Installing
Clone this repository and install the required libraries using the following command:

`pip install pinpong bleak`

### Usage
Connect your Unihiker robot to your computer and run the following command to start the script(or launch it from interne menu):

`python bluetooth_flooder.py`

Please note that this program is for educational purposes only, and should not be used to flood or attack Bluetooth devices without proper authorization.
