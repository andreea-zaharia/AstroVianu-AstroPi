#library import
from sense_hat import SenseHat
from datetime import datetime
import time

#variable initialization
sense = SenseHat()
FILENAME = ""
WRITE_FREQUENCY = 10 
recal = 0 #used to know when new mean data is needed (to be set as threshold)
CALIBRATION_TIME = 900 #time of recalibration
EPSILON = 0.2 #smallest vibration variation for detecting human presence 
notFirstLoop = 0 #prevents the led matrix from turning on when the loops runs for the first time
sleepTime = 0.5 
mTemp = 0 #mean temperature
mHum = 0 #mean humidity
mPres = 0 #mean Pressure
lastPitch = 0
deltaPitch = 0
lastYaw = 0
deltaYaw = 0
lastRoll = 0
deltaRoll = 0
lastAction = 0
startTime = time.clock() #time at the start of program
humanPresence = 0

ye = [255, 255, 0]  # yellow
bl = [0, 0, 0]  # blank
green = [0, 255, 0]
red = [255, 0, 0]
smiley_face = [
bl, bl, bl, bl, bl, bl, bl, bl,
bl, ye, ye, bl, bl, ye, ye, bl,
bl, ye, ye, bl, bl, ye, ye, bl,
bl, bl, bl, bl, bl, bl, bl, bl,
ye, bl, bl, bl, bl, bl, bl, ye,
bl, ye, bl, bl, bl, bl, ye, bl,
bl, bl, ye, ye, ye, ye, bl, bl,
bl, bl, bl, bl, bl, bl, bl, bl
]

winky_face = [
bl, bl, bl, bl, bl, bl, bl, bl,
bl, bl, bl, bl, bl, ye, ye, bl,
bl, ye, ye, bl, bl, ye, ye, bl,
bl, bl, bl, bl, bl, bl, bl, bl,
ye, bl, bl, bl, bl, bl, bl, ye,
bl, ye, bl, bl, bl, bl, ye, bl,
bl, bl, ye, ye, ye, ye, bl, bl,
bl, bl, bl, bl, bl, bl, bl, bl
]

sad_face = [
bl, bl, bl, bl, bl, bl, bl, bl,
bl, red, red, bl, bl, red, red, bl,
bl, red, red, bl, bl, red, red, bl,
bl, bl, bl, bl, bl, bl, bl, bl,
bl, bl, red, red, red, red, bl, bl,
bl, red, bl, bl, bl, bl, red, bl,
red, bl, bl, bl, bl, bl, bl, red,
bl, bl, bl, bl, bl, bl, bl, bl
]

#gets data from sensors and appends them to sense_data
def getSenseData():
    senseData=[] 
    sense.set_imu_config(True, False, False)
    t = round(sense.get_temperature(), 2)
    h = round(sense.get_humidity(), 2)
    p = round(sense.get_pressure(), 2)
    comp = sense.get_compass()
    rawComp = sense.get_compass_raw()
    
    senseData.append(datetime.now())
    senseData.append(t)
    senseData.append(h)
    senseData.append(p)
    senseData.append(comp)
    senseData.append(rawComp)
    
    return senseData

#setup for file header
def fileSetup(filename):
  header = ["timestamp", "temperature", "humidity", "pressure", "magnetic intensity", "magnetic intensity on axes", "pitch", "yaw", "roll"]

  with open(filename,"w") as f:
      f.write(" || ".join(str(value) for value in header) + "\n")

#prints data appended in sense_data
def printData():
    outputString = ", ".join(str(value) for value in senseData)
    batchData.append(outputString)
    
#runs every CALIBRATION_TIME seconds in order to obtain new mean values
def calibration():
    time0 = time.clock()
    time1 = time.clock()
    counter = 0

    global mTemp, mHum, mPres 
    
    while time1 - time0 <= 60.0:
        t = round(sense.get_temperature(), 2)
        h = round(sense.get_humidity(), 2)
        p = round(sense.get_pressure(), 2)

        mTemp += t
        mHum += h
        mPres += p
        counter += 1
        time1 = time.clock()
        
    mTemp /= counter
    mHum /= counter
    mPres /= counter
    
#gets orientation
def getOrientation():

    global lastPitch, deltaPitch, lastYaw, deltaYaw, lastRoll, deltaRoll
    sense.set_imu_config(False, True, True)
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    
    pitch = round(pitch, 1)
    roll = round(roll, 1)
    yaw = round(yaw, 1)
    senseData.append(pitch)
    senseData.append(yaw)
    senseData.append(roll)

    deltaPitch = abs(lastPitch - pitch)
    deltaYaw = abs(lastYaw - yaw)
    deltaRoll = abs(lastRoll - roll)

    lastPitch = pitch
    lastYaw = yaw
    lastRoll = roll
    #print(pitch, yaw, roll)
    

#writes to file with timestamp
batchData = []

if FILENAME == "":
  filename = "SenseLog-" + str(datetime.now()) + ".csv"
else:
  filename = FILENAME + "-" + str(datetime.now()) + ".csv"

fileSetup(filename)



while True:

    currentTime = time.clock()
    if currentTime - startTime > recal and humanPresence == 0:
        calibration()
        recal += CALIBRATION_TIME

    humanPresence = 0;
    
    senseData = getSenseData()
    getOrientation()

    #print(deltaPitch, deltaYaw, deltaRoll)
    
    
    if notFirstLoop == 1 and ((deltaPitch > EPSILON or deltaYaw > EPSILON or deltaRoll > EPSILON) or senseData[2] >= mHum + 4):
        humanPresence = 1
        sense.set_pixels(smiley_face)
        lastAction = 10
        
    notFirstLoop = 1
    printData()
    time.sleep(sleepTime)
    lastAction -= 1
    if lastAction <= 5 and lastAction > 0:
        sense.set_pixels(winky_face)
    if lastAction <= 0:
        sense.set_pixels(sad_face)
    if len(batchData) >= WRITE_FREQUENCY:
      print("Writing to file...")
      with open(filename,"a") as f:
          for line in batchData:
              f.write(line + "\n")
          batchData = []

    
