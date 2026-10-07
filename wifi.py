import network

wlan = network.WLAN()       # create station interface (the default, see below for an access point interface)
wlan.active(True)           # activate the interface
wlan.scan()                 # scan for access points
connect = wlan.isconnected()

print(connect)