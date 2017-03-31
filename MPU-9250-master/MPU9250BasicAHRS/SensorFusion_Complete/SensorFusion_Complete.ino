/* Code for the MPU9250 class is written by Kris Weiner
 date: April 1, 2014
 license: Beerware - Use this code however you'd like. If you
 find it useful you can buy me a beer some time.
 Modified by Brent Wilkins July 19, 2016

 Hardware setup:
 MPU9250 Breakout --------- Arduino
 VDD ---------------------- 3.3V
 VDDI --------------------- 3.3V
 SDA ----------------------- SDA
 SCL ----------------------- SCL
 GND ---------------------- GND
 */

#include <Arduino.h>
#include <SPI.h>
#if not defined (_VARIANT_ARDUINO_DUE_X_) && not defined(ARDUINO_ARCH_SAMD)
  #include <SoftwareSerial.h>
#endif
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#include "BluefruitConfig.h"

#include "quaternionFilters.h"
#include "MPU9250.h"
#include "Wire.h"

#include "kNN.h"

#define AHRS true         // Set to false for basic data read
#define SerialDebug false  // Set to true to get Serial output for debugging
#define Graphing true      // Set to get graphing data
#define flexSensors true   // Set to true if flex sensors attached
#define bluetooth true      // Set to true if Bluetooth is enabled

// helper functions

void error(const __FlashStringHelper*err) {
  Serial.println(err);
  while (1);
}

void I2Cscan() {
  // scan for i2c devices
  byte error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) 
  {
    Serial.println(address);
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.print(address,HEX);
      Serial.println("  !");
      nDevices++;
    }
    else if (error==4) 
    {
      Serial.print("Unknown error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");
}

// Pin definitions and globals
int thumb = 1;
const int idx = 2;
int middle = 3;
int ring = 4;
int pinky = 5;
int frequency = 1;
char message[33];

kNN knn;

MPU9250 myIMU;

/* ...hardware SPI, using SCK/MOSI/MISO hardware */
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

void setup()
{
  Wire.begin();
  Serial.begin(38400);
  
  if ( !ble.begin(VERBOSE_MODE) ) {
    error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
  
  /* Disable command echo from Bluefruit */
  ble.echo(false);

  /* Change the device name to make it easier to find */
  if (! ble.sendCommandCheckOK(F( "AT+GAPDEVNAME=Sensor Glove" )) ) {
    error(F("Could not set device name?"));
  }

  // Set to Data Mode
  ble.setMode(BLUEFRUIT_MODE_DATA);
  
// I2Cscan is a helpful function for troubleshooting MPU9250 connection
// I2Cscan();

  // Read the WHO_AM_I register, this is a good test of communication
  byte c = myIMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);

// Uncomment below for debugging
//  Serial.print("MPU9250 "); Serial.print("I AM "); 
//  Serial.print(c, HEX); Serial.print(" I should be "); 
//  Serial.println(0x71, HEX);

  if (c == 0x71) // WHO_AM_I should always be 0x68
  {
//    Serial.println("MPU9250 is online...");

    // Start by performing self test and reporting values
    myIMU.MPU9250SelfTest(myIMU.SelfTest);

    // Calibrate gyro and accelerometers, load biases in bias registers
    myIMU.calibrateMPU9250(myIMU.gyroBias, myIMU.accelBias);

    myIMU.initMPU9250();
    // Initialize device for active mode read of acclerometer, gyroscope, and
    // temperature

    // Read the WHO_AM_I register of the magnetometer
    byte d = myIMU.readByte(AK8963_ADDRESS, WHO_AM_I_AK8963);

    // Get magnetometer calibration from AK8963 ROM
    myIMU.initAK8963(myIMU.magCalibration);
    // Initialize device for active mode read of magnetometer

  } // if (c == 0x71)
  else
  {
    Serial.print("Could not connect to MPU9250: 0x");
    Serial.println(c, HEX);
    while(1) ; // Loop forever if communication doesn't happen
  }
}

void loop()
{
  // If intPin goes high, all data registers have new data
  // On interrupt, check if data ready interrupt
  if (myIMU.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)
  {  
    myIMU.readAccelData(myIMU.accelCount);  // Read the x/y/z adc values
    myIMU.getAres();

    // Now we'll calculate the accleration value into actual g's
    myIMU.ax = (float)myIMU.accelCount[0]*myIMU.aRes; // - accelBias[0];
    myIMU.ay = (float)myIMU.accelCount[1]*myIMU.aRes; // - accelBias[1];
    myIMU.az = (float)myIMU.accelCount[2]*myIMU.aRes; // - accelBias[2];

    myIMU.readGyroData(myIMU.gyroCount);  // Read the x/y/z adc values
    myIMU.getGres();

    // Calculate the gyro value into actual degrees per second
    myIMU.gx = (float)myIMU.gyroCount[0]*myIMU.gRes;
    myIMU.gy = (float)myIMU.gyroCount[1]*myIMU.gRes;
    myIMU.gz = (float)myIMU.gyroCount[2]*myIMU.gRes;

    myIMU.readMagData(myIMU.magCount);  // Read the x/y/z adc values
    myIMU.getMres();
    myIMU.magbias[0] = +470.;
    myIMU.magbias[1] = +120.;
    myIMU.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Get actual magnetometer value, this depends on scale being set
    myIMU.mx = (float)myIMU.magCount[0]*myIMU.mRes*myIMU.magCalibration[0] -
               myIMU.magbias[0];
    myIMU.my = (float)myIMU.magCount[1]*myIMU.mRes*myIMU.magCalibration[1] -
               myIMU.magbias[1];
    myIMU.mz = (float)myIMU.magCount[2]*myIMU.mRes*myIMU.magCalibration[2] -
               myIMU.magbias[2];
  } // if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)

  // Must be called before updating quaternions!
  myIMU.updateTime();

//  MadgwickQuaternionUpdate(ax, ay, az, gx*PI/180.0f, gy*PI/180.0f, gz*PI/180.0f,  my,  mx, mz);
  MahonyQuaternionUpdate(myIMU.ax, myIMU.ay, myIMU.az, myIMU.gx*DEG_TO_RAD,
                         myIMU.gy*DEG_TO_RAD, myIMU.gz*DEG_TO_RAD, myIMU.my,
                         myIMU.mx, myIMU.mz, myIMU.deltat);

  if (!AHRS)
  {
  } // if (!AHRS)
  else
  {
    myIMU.delt_t = millis() - myIMU.count;

    if (myIMU.delt_t > 1000/frequency)
    {

    // Define output variables from updated quaternion---
    // these are Tait-Bryan angles, commonly used in aircraft 
    // orientation. In this coordinate system, the positive 
    // z-axis is down toward Earth. Yaw is the angle between Sensor
    // x-axis and Earth magnetic North (or true North if corrected 
    // for local declination, looking down on the sensor positive 
    // yaw is counterclockwise. Pitch is angle between sensor 
    // x-axis and Earth ground plane, toward the Earth is positive, 
    // up toward the sky is negative. Roll is angle between sensor 
    // y-axis and Earth ground plane, y-axis up is positive roll. 
    // These arise from the definition of the homogeneous rotation 
    // matrix constructed from quaternions. Tait-Bryan angles as well 
    // as Euler angles are non-commutative; that is, to get the correct 
    // orientation the rotations must be applied in the correct order 
    // which for this configuration is yaw, pitch, and then roll.
      myIMU.yaw   = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                    *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * 
                    *(getQ()+1)
                    - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * 
                    *(getQ()+3));
      myIMU.pitch = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                    *(getQ()+2)));
      myIMU.roll  = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                    *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * 
                    *(getQ()+1) - *(getQ()+2) * *(getQ()+2) + 
                    *(getQ()+3) * *(getQ()+3));
      myIMU.pitch *= RAD_TO_DEG;
      myIMU.yaw   *= RAD_TO_DEG;
      myIMU.yaw   -= 8.5;
      myIMU.roll  *= RAD_TO_DEG;
      
      int test_p[] = {analogRead(thumb),analogRead(idx),analogRead(middle)
                      ,analogRead(ring),analogRead(pinky)};
      float test_o[] = {myIMU.roll,myIMU.pitch,myIMU.yaw};
      int result = knn.run(test_p, test_o);
      
      if (bluetooth) {  // Send Gesture as a string over bluetooth
        char command[]="AT+BLEUARTTXF";
        sprintf(message,"%s=%i",command,result);
        if (ble.atcommand(F("AT+BLEGETRSSI")) != 0) {
          ble.atcommand(F(message));
        }
      }
      else {  // Otherwise print to the serial port
        Serial.println(result);
      }

      myIMU.count = millis();
      myIMU.sumCount = 0;
      myIMU.sum = 0;
    } // if (myIMU.delt_t > 50)
  } // if (AHRS)
} // Loop

