# AstroVianu-AstroPi
AstroVianu Team's code for the Astro Pi European Challenge 2017

## Primary Mission - Human Presence Detection in the ISS Columbus Module
- makes use of the accelerometer, gyroscope, and the humidity sensor
- signals the detection by showing a smiley and winking face on the 8x8 pixel display; when no human is detected, the matrix displays a red sad face

### Algorithm Description
- always compares the current pitch, roll, and yaw readings with the ones taken 0.5 seconds ago; if the absolute delta is above a certain constant which we have found empirically, then human presence has been detected
- gets the air humidity readings from the sensor every CALIBRATION_TIME for 60 seconds and calculates their mean (mHum) inside the "calibration()" function; while it is not calibrating, it compares the current humidity level to mHum - if the current reading is more than 4% higher (confidence interval of the sensor), then a human is nearby
- has a global flag, humanPresence, tracking the state of the detection activity, which is equal to one if an astronaut is currently in the module - the calibration subprogram will not run while an astronaut is in the module

## Secondary Mission - Magnetic Field Study
### Data Acquistion Code Description
- measures the magnetic induction (in microteslas), on the three axes, x, y and z, and the direction of North, in degrees, using the incorporated magnetometer
- keeps track of the data from the IMU, to calculate the acceleration. 
- creates a table printing for each measurement the said magnetic induction on axes, along with the full timestamp corresponding to the exact time. Although we use only the accelerometer and the magnetometer in this mission per se, the code is also going to provide in the same table data collected using the environmental sensors (temperature, pressure and humidity), since we would be interested to research more and observe if there are any other parameters that might change, which are not part of the mission we have chosen. 
