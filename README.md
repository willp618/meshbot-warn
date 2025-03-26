# MeshBot

![Meshbot](./img/meshbot.png)
THIS IS A VERSION THAT CAN PULL FLOOD WARNINGS FROM https://environment.data.gov.uk/flood-widgets/rss-feeds.html 
THE CODE IS MIXTURE OF MY OWN AND CHATGPT 
BE WARNED IT MIGHT NOT WORK RIGHT
MeshBot is an OpenSource Python program designed to run on computers with a connected Meshtastic device, allowing users to send and receive messages efficiently over a mesh network.

Our Mission: 
 - To provied low-bandwidth functionality to a low bandwidth mesh.  This has originated in the EU where we have 1x longfast channel, and 10% duty cycle, so we try hard to make this low bandwidth, efficent, purposeful and helpful.  
 - For those outside of the EU, knock yourselves out, its opensource, modify at will. Just please dont be offended if we reject high bandwidth pull-requests, but we have no issues with extending commands.
 - As we are open source and an open community, please publish and share your meshtastic work. 

## Features

- Broadcast messages: Send text broadcasts to all devices on the mesh network.
- Weather updates: Get real-time weather updates for a specified location.
- Tides information: Receive tidal information for coastal areas.
- Whois: Query one of two User databases: mpowered247 or liamcottle
- Simple BBS: Store and retrieve messages via the bot

Requirements
Python 3.x
Meshtastic Python library
Access to a Meshtastic device Meshtastic
Serial drivers for your meshtastic device, See Installing Serial Drivers
Installation
Clone this repository to your local machine:
git clone https://github.com/868meshbot/meshbot.git   IGNORE THIS JUST GO TO STEP 2
Navigate into the folder and setup a virtual environment
cd meshbot
python3 -m venv .venv
. .venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt
Connect your Meshtastic device to your computer via USB and run the program
python ./meshbot.py
Configuration (NEW)
We have revamped the configuration, there is now a ''settings.yaml'' file, which we believe makes the program easier to manage

Example Content:

---
LOCATION: "kidderminster" #wx1
LOC2: "Bridgnorth" #wx2
LOC3: "worcester"#wx3
TIDE_LOCATION: "Swansea"
MYNODE: "3663493700"
MYNODES:
  - "3663493700"
  - "1234567890"
DBFILENAME: "./db/nodes.db"
DM_MODE: True
FIREWALL: True
DUTYCYCLE: True
Description

LOCATION and TIDE_LOCATION = These should be obvious
MYNODE = The hw address of the node connected in int/number form. This is so the bot only responds to DMs GET THIS FROM LIAMS COTTLES MAP UNDER NODE ID
MYNODES = A list of nodes (in int/number form) that are permitted to interact with the bot
DBFILENAME = Configure which user database file to use by default
DM_MODE = True: Only respond to DMs; False: responds to all traffic
FIREWALL = True: Only respond to MYNODES; False: responds to all traffic
DUTYCYCLE: True: Respect 10% Dutycycle in EU, false to disable for countries without Dutycycle
Usage
Run the MeshBot program:

python meshbot.py --help
Example on Linux:

python meshbot.py --port /dev/ttyUSB0
Example on OSX:

python meshbot.py --port /dev/cu.usbserial-0001
Example on Windows:

python meshbot.py --port COM7
Example using TCP client:

python meshbot.py --host meshtastic.local
or
python meshbot.py --host 192.168.0.100
Bot interaction
You bot will be accessible through the meshtastic mesh network through the node name. DM the bot/node and issue any of the following commands:

#test : receive a test message CHANGED FOR LOCALS SORRY
#ping : as #test above only more detail e.g snr,rssi, hop count (thanks to rohanki) CHANGE IT FROM #tst-detail BECAUSE PING JUST MAKES MORE SENSE
#wx1-3 : local weather report WITH MORE DETAIL THAN BEFORE
#tides : tide info (dont forget to change the default town in the source)
#whois #xxxx : retrieve name and node info for a node based on last 4 chars of address
#bbs any : do I have any messages?
#bbs post !address message : post a message on the bbs for a given user at !address
#bbs get : retrieve your message(s) left by another user(s)
#flood GETS FLOOD WARNINGS VIA RSS
#wxwarn GETS WX WARNINGS VIA RSS MIGHT NOT WORK
#hi SENDS "hello there"
#local SENDS https://willp618.github.io/magenta-briana-21/
#dx SENDS https://willp618.github.io/crimson-margeaux-37/
#awake SENDS "yes the bot is awake" done as a test thing when i was working out things
Contributors
868meshbot
Acknowledgements
This project utilizes the Meshtastic Python library, which provides communication capabilities for Meshtastic devices. For more information about Meshtastic, visit meshtastic.org.

License
This project is licensed under the MIT License - see the LICENSE file for details.

References
Database of IDs, long_name and short_names obtained from the node list from the following URLs:

https://map.mpowered247.com/
https://meshtastic.liamcottle.net/
## References

Database of IDs, long_name and short_names obtained from the node list from the following URLs:

- [https://map.mpowered247.com/](https://map.mpowered247.com/)
- [https://meshtastic.liamcottle.net/](https://meshtastic.liamcottle.net/)
