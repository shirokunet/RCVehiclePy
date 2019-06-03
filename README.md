# RCVehiclePy
This is a Tool to Control steering and throttle of a R/C car via MQTT with Raspberry Pi 3B.

[![demo_off_road](https://raw.githubusercontent.com/wiki/shirokunet/RCVehiclePy/images/off_road.gif)](https://www.youtube.com/watch?v=wb1s7gsLcVM)


## Table of Contents
   * [Prepare Hardware](#Prepare-Hardware)
   * [Getting Started](#Getting-Started)
   * [Demo](#Demo)
   * [Acknowledgments](#Acknowledgments)
   * [License](#License)


## Prepare Hardware
### Setup Raspberry Pi 3B
- You can read my simple instruction at [here](https://shiroku.net/robotics/raspberry-pi-3b-setup/).

### Build a car
<img src="https://raw.githubusercontent.com/wiki/shirokunet/RCVehiclePy/images/overview.jpg" width="672">

- Hardware is almost same as a [Donkey Car](http://docs.donkeycar.com/guide/build_hardware/).
- I bought below parts. The cost is about $130.
    * $84.95 [Exceed Racing Desert Short Course Truck 1/16 Scale Ready to Run 2.4ghz (AA Blue)](https://www.amazon.com/dp/9269802086/)
    * $28.84 [Raspberry Pi Camera Module V2-8 Megapixel,1080p](https://www.amazon.com/dp/B01ER2SKFS/)
    * $9.99 [SunFounder PCA9685 16 Channel 12 Bit PWM Servo Driver for Arduino and Raspberry Pi](https://www.amazon.com/dp/B014KTSMLA/)
    * $6.98 [Maxmoral 2 Set (40P/Set) 10cm Female to Female Jumper Wire](https://www.amazon.com/dp/B010L30SE8/)

### Access point
We have several ways to connect Host PC and Raspberry Pi in outside.
- Setting Raspberry Pi as an access point. [(documentation)](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
- Put a smart phone on a R/C car, and tethering both of them. 
- Put a mobile wifi router on a R/C car. 


## Getting Started
### Connect to Pi via SSH
After setup access points,
```
$ sudo ssh pi@raspberrypi.local
```

### Setup momo
Momo is a powerfuil WebRTC Native Client. You can follow my instraction at [here](https://shiroku.net/robotics/run-webrtc-native-client-momo-on-raspberry-pi-3b/).

### Clone Repository
```
$ cd ~/
$ git clone https://github.com/shirokunet/RCVehiclePy
```

### Update pip3 (optional)
```
$ sudo apt-get remove python-pip python3-pip
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
```

### Setup Prerequisites
- Python 3.5.x
- numpy 1.16.1
- PyYAML 3.12

```
$ cd ~/RCVehiclePy/
$ sudo pip3 install -r requirements.txt
$ sudo apt-get install python3-numpy
$ sudo apt-get install python3-yaml
```

### Check Pi's IP address
```
$ ifconfig
    wlan0: flags=4163 mtu 1500
    inet xx.xx.xx.xx netmask 255.255.255.0
```

### Setup config file
Then chenge config file
```
$ cd ~/RCVehiclePy/
$ vi config.yml
pi_ip: 'xx.xx.xx.xx'
```

### Lunch MQTT publisher on the Raspberry Pi

```
$ cd ~/RCVehiclePy/
$ python3 pi_main.py
```

### Set environment on the host PC
Same as the step of the Raspberry Pi.
- [Clone Repository](#clone-repository)
- [Setup Prerequisites](#setup-prerequisites)
- [Setup config file](#setup-config-file)

### Lunch MQTT publisher on the host PC

```
$ cd ~/RCVehiclePy/
$ python3 pc_main.py
```

### Send command to Pi from the host PC
Just push key "UP" or "DOWN" or "LEFT" or "RIGHT" on the terminal.

### Stop Program
Type 'Ctrl' + 'c' in both terminals.


## Demo
The latency is about 100~300msec. It can be controlled easily even if you watch only the camera streaming.
[![demo_flat_road](https://raw.githubusercontent.com/wiki/shirokunet/RCVehiclePy/images/flat_road.gif)](https://www.youtube.com/watch?v=Y4eQZay4Up8)

[![camera_flat_road](https://raw.githubusercontent.com/wiki/shirokunet/RCVehiclePy/images/flat_road_cam.gif)](https://www.youtube.com/watch?v=cbQFkdlA74Y)


## Acknowledgments

* [Actuator layer](https://github.com/shirokunet/RCVehiclePy/blob/master/parts/actuator.py) is built upon [autorope/donkeycar](https://github.com/autorope/donkeycar). Thank you!


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

