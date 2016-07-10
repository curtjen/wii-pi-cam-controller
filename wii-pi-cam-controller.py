#!/usr/bin/python
# Wii-Pi-Cam-Controller
# Project:
# https://github.com/curtjen/wii-pi-cam-controller

# Wiimote controls based off of:
# http://www.raspberrypi-spy.co.uk/?p=1101

import cwiid, time, os, re, subprocess

button_delay = 0.1
mode = 'movie'

# Connect camera
print 'Connecting camera....'

def cam_connect():
    getSummary = subprocess.Popen(['gphoto2', '--summary'], stdout=subprocess.PIPE)
    camOutput = getSummary.stdout.read()
    searchObj = re.search( r'error', camOutput, re.M|re.I )

    if searchObj:
        print 'Camera not connected...'
    else:
        set_capturetarget()
        print "Camera connected successfully"


def set_capturetarget():
    getCaptureTarget = subprocess.Popen(['gphoto2', '--get-config', 'capturetarget'], stdout=subprocess.PIPE)
    camOutput = getCaptureTarget.stdout.read()
    searchObj = re.search( r'Current: Memory card', camOutput, re.M|re.I )

    if not searchObj:
        os.system('gphoto2 --set-config capturetarget=1')
        print "gphoto2 capturetarget set to Memory card"
    else:
        print "gphoto2 capturetarget already set to Memory card"


def change_setting(setting, upDown):
    # Get config setting
    getConfigOutput = subprocess.Popen(['gphoto2', '--get-config', setting], stdout=subprocess.PIPE)

    # Turn the config setting output into an array
    getConfigOutputList = getConfigOutput.stdout.read().split('\n')

    configList = []

    # Convert each getConfigOutputList item into subarrays
    for line in getConfigOutputList:
        item = line.split(' ')
        configList.append(item)


    # Get current index
    current = configList[2][1]
    rangeList = []

    # Get list of choices
    for line in configList:
        if line[0] == 'Choice:':
            rangeList.append( int(line[1]) )
            if current == line[2]:
                currentIndex = int(line[1])

    if upDown == 'up':
        print upDown
        print "Matching currentIndex: %s" % currentIndex

        if currentIndex + 1 < rangeList[-1]:
            newIndex = currentIndex + 1
            os.system('gphoto2 --set-config %s=%s' % (setting, newIndex))
        else:
            newIndex = currentIndex

        print "Matching newIndex: %s" % newIndex

    if upDown == 'down':
        print upDown
        print "Matching currentIndex: %s" % currentIndex

        if currentIndex - 1 >= rangeList[0]:
            newIndex = currentIndex - 1
            os.system('gphoto2 --set-config %s=%s' % (setting, newIndex))
        else:
            newIndex = currentIndex

        print "Matching newIndex: %s" % newIndex


def toggle_mode(m):
    global mode

    if m == 'movie':
        mode = 'image'

    elif m == 'image':
        mode = 'movie'

    print "Mode set to: %s" % mode
    # return mode


def movie_start_stop():
    getMovieRecordTarget = subprocess.Popen(['gphoto2', '--get-config', 'movierecordtarget'], stdout=subprocess.PIPE)
    stopMovieStatus = getMovieRecordTarget.stdout.read()
    searchObj = re.search( r'Current: Card', stopMovieStatus, re.M|re.I )

    # If video is already recording then stop
    if (searchObj):
        os.system('gphoto2 --set-config movierecordtarget=None')
    # Else start recording
    else:
        os.system('gphoto2 --set-config viewfinder=1 --set-config movierecordtarget=Card')


try:
    camera = cam_connect()
except RuntimeError:
    print "Error connecting camera"
    raise SystemExit

# Connect to the Wii Remote. If it times out then quit.

print 'Press sync button on your Wii Remote now...'
time.sleep(1)

while True:
    try:
        global wii
        wii = cwiid.Wiimote()
        break
    except RuntimeError:
        print 'Timeouted out. Trying again.'


print 'Wii Remote connected...\n'
wii.rumble = 1
time.sleep(1)
wii.rumble = 0
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

wii.rpt_mode = cwiid.RPT_BTN
 
while True:

    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed
    # together then rumble and send shutdown command.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print '\nClosing connection ...'
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        os.system('shutdown -h now')
    
    # Check if other buttons are pressed by
    # doing a bitwise AND of the buttons number
    # and the predefined constant for that button.
    if (buttons & cwiid.BTN_LEFT):
        change_setting('shutterspeed', 'down')
        print 'Left pressed'
        time.sleep(button_delay)

    if(buttons & cwiid.BTN_RIGHT):
        change_setting('shutterspeed', 'up')
        print 'Right pressed'
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_UP):
        change_setting('aperture', 'up')
        print 'Up pressed'
        time.sleep(button_delay)
        
    if (buttons & cwiid.BTN_DOWN):
        change_setting('aperture', 'down')
        print 'Down pressed'
        time.sleep(button_delay)
        
    if (buttons & cwiid.BTN_1):
        toggle_mode('movie')
        print 'Button 1 pressed'
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_2):
        toggle_mode('image')
        print 'Button 2 pressed'
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_A):
        if mode == 'movie':
            movie_start_stop()
            print 'Button A pressed'
            time.sleep(button_delay)

        elif mode == 'image':
            # Capture image
            os.system('gphoto2 --capture-image')

        else:
            print "The mode is: %s" % mode

    if (buttons & cwiid.BTN_B):
        if mode == 'movie':
            movie_start_stop()
            print 'Button A pressed'
            time.sleep(button_delay)

        elif mode == 'image':
            # Capture image
            os.system('gphoto2 --capture-image')

        else:
            print "The mode is: %s" % mode

        print 'Button B pressed'
        time.sleep(button_delay)

    if (buttons & cwiid.BTN_HOME):
        print 'Home Button pressed'
        time.sleep(button_delay)
        
    if (buttons & cwiid.BTN_MINUS):
        change_setting('iso', 'down')
        print 'Minus Button pressed'
        time.sleep(button_delay)
        
    if (buttons & cwiid.BTN_PLUS):
        change_setting('iso', 'up')
        print 'Plus Button pressed'
        time.sleep(button_delay)
