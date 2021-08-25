import RPi.GPIO as GPIO  # Import GPIO library
import time
import sys
import os
import subprocess
import multiprocessing
import shutil
import threading
MAX_COPY_NUMBER = 20

# sleep of 10 seconds @ startup to let all the drives get mounted
time.sleep(10)

# GPIO setup for led and btn
BUTTON_PRESS_DURATION = 0.5
buttonPin = 11
ledPin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)  # Setup GPIO Pin 7 to OUT

# LED Functions
def destroy():
  GPIO.output(ledPin, GPIO.LOW)   # led off
  GPIO.cleanup(ledPin)      

def led_control(state, speed):
    destroy()
    GPIO.setup(ledPin, GPIO.OUT)
    if(state == 'on'):
        GPIO.output(ledPin, True)  # Turn on GPIO pin 7
    elif(state == 'off'):
        GPIO.output(ledPin, False)  # Turn off GPIO pin 7
    elif(state == 'blink'):
        if(speed == 'fast'):
            delay = 0.1
        elif(speed == 'normal'):
            delay = 0.4
        elif(speed == 'slow'):
            delay = 2
        else:
            delay = speed
        while True:
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            time.sleep(delay)
            GPIO.output(ledPin, GPIO.LOW)  # led off
            time.sleep(delay)

led_control_processes = []
def control_led(state, speed):
    if not len(led_control_processes):
        p = multiprocessing.Process(
            target=led_control, args=[state, speed])
        led_control_processes.append(p)
        p.start()
    else:
        led_control_processes[-1].kill()
        p = multiprocessing.Process(
            target=led_control, args=[state, speed])
        led_control_processes.append(p)
        p.start()


# function to wait for btn press

def wait_for_btn_press(reason):
    print('waiting for btn press {0} ...'.format(reason))
    while True:
        input_state = GPIO.input(buttonPin)
        time.sleep(BUTTON_PRESS_DURATION)
        if input_state == False:
            # button pressed
            print('btn pressed! for {0} ...'.format(reason))
            break


# get list of mountpoints

def get_mpoints_list():
    # get list of mountpoints
    with open('mpoints.txt', 'w') as f:
        f.write(subprocess.getoutput(
            "df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $1 }'|tail -n +3"))

    drives_txt_file = open('mpoints.txt', 'r')
    drives_list = [line.split() for line in drives_txt_file.readlines()]
    return drives_list

# Mount all   -- UNFINISHED --

def mount_usb_drives():
    mpoints_list = get_mpoints_list()
    for mpoint in mpoints_list:
        print(mpoint)


# get list of usb drives

def get_drives_list():
    # get list of usb drives
    with open('drives.txt', 'w') as f:
        f.write(subprocess.getoutput(
            "df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $6 }'|tail -n +3"))

    drives_txt_file = open('drives.txt', 'r')
    drives_list = [line.split() for line in drives_txt_file.readlines()]
    return drives_list

# CHECK FOR COPY STATE
# CHK IF COPY DONE

def is_copy_done():

    drives_list = get_drives_list()
    # check if data is already copied with existance of text file
    copy_completed = None
    for drive in drives_list:
        if(os.path.isfile('{}/copy_completed.txt'.format(*drive, sep=", "))):
            # start fastblinking to denote copy done
            copy_completed = True
        else:
            # start copy process
            copy_completed = False
            break
    return copy_completed



# copy count functions
def set_copy_count(x):
    file = open('count.txt', 'w')
    return(file.write(str(x)))

def get_copy_count():
    file = open('count.txt', 'r')
    return(int(file.read()))


# Abstract rmtree
def rmtree(drive):
    try:
        shutil.rmtree(drive)
    except:
        print(drive)
        print('completed Empty Process!')

# Empty drives operation
def empty_drives():
    drives_list = get_drives_list()

    processes_list = []
    for drive in drives_list:
        drive = str(drive)[2:-2]
        p = multiprocessing.Process(target=rmtree, args=[drive])
        processes_list.append(p)
        p.start()
    
    for p in processes_list:
        p.join()


# abstraction of copytree command
def copytree(source,dest):
    copy_completed_dir_path = '/home/pi/copy_completed.txt'
    shutil.copytree(source, dest, dirs_exist_ok=True)
    shutil.copy(copy_completed_dir_path, dest)

def copy_operation():
    # Define source directory
    source_dir = '/home/pi/src'
    drives_list = get_drives_list()
    copy_processes = []
    for drive in drives_list:
        drive = (str(drive)[2:-2])
        p = multiprocessing.Process(target=copytree(source_dir, drive))
        p.start()
        copy_processes.append(p)

    for process in copy_processes:
        process.join()


#----------- init ---------#
# Program initialization
def init():
    if(is_copy_done()):
        # fastblink led to denote files are already copied
        control_led('blink', 'fast')
        wait_for_btn_press('copy done')
        init()
    else:
        control_led('on', '')
        wait_for_btn_press('copy not done')
        # start copy process
        control_led('blink','normal')
        # format process
        empty_drives()
        #copy_operation()   # Use in python version 3.9 or above only
        subprocess.call(['./copy.sh'])    #use in python 3.7 or lower versions
        #set_copy_count(get_copy_count()+1)
        init()

# ------- Initializing pr0gram ---------- #
init()
        






