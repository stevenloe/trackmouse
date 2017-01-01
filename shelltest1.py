import time
from subprocess import call

print("Starting TrackMouse")
print("Start GPS Daemon and wait 3 seconds...")

call(["sudo", "gpsd", "/dev/ttyUSB0", "-F", "/var/run/gpsd.sock"])
# sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

time.sleep(3)
print("finished!!")

# call(["cgps", "-s"])
