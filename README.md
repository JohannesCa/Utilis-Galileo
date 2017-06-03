UTILIS-GALILEO
==============

This is an application written in python to implement a web server within an Intel Galileo board. Simplifies GPIO interface with implemented classes and webcam stream with OpenCV.


REQUIREMENTS
------------

- Python 2.7 is recommended.
- OpenCV
- Flask


SETUP/PIN CONFIGURATION
-----------------------

To setup devices table you should edit ['_pins.csv_'](https://github.com/JohannesCa/Utilis-Galileo/blob/master/pins.csv "pins.csv") in the following format

>pin,device_name,device_type

where *pin* is the physical pin number in Galileo board (it'll do an internal mapping to GPIO), *device_name* is the desired device's name and *device_type* is the device's type witch can be '_out_' (digital) or '_analog_'.


RUNNING
-------

To run the application run

>$ python main.py

It should initialize the server at **localhost:3000**.


ACKNOLODGEMENTS
---------------

This project was originally merged with the [**Utilis Project**](https://github.com/samuelpordeus/utilis "Utilis") and was made for an Embedded Systems discipline at Informatics Center, UFPB.