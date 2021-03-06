# Composition Generator

This project allows a user to create Mondrian style compositons consisting of his famous lines and boxes, and using only a handful of bright colors. [*Composition with Red Blue and Yellow*](https://en.wikipedia.org/wiki/Composition_with_Red_Blue_and_Yellow "Composition with Red Blue and Yellow") is such an example. This project allows a user to create those both through their actions, but with randomness as well. Here is a [video](https://youtu.be/f7O3wUGoslw) of the project in action. An ESP32 is connected to a breadboard, which has two buttons. One button randomly chooses a color, and one button randomly chooses a drawing direction. The setup is completely wireless and communication from the ESP32 to the code is done through a UDP socket. 
## Hardware Setup
The following hardware is used for the setup:
- ESP32 GPIO Extension Board
- Breadboard
- Two buttons
- One 3.7 V 650 mA rechargeable battery
- Wires

The two buttons go onto the breadboard and are then each connected with two wires. One wire goes from one of the metal legs of the button to GND. Then the other wire will connect to one of the numbered GPIO pins to the ESP32. I used GPIO pins 18 and 32 for this project, however others could be used. Just make sure that in `input.ino` you set the correct GPIO numbers. Optionally, this setup uses a battery so the device can work wirelessly (although this is optional and you can plug the ESP32 into your laptop or some other power source if you do not want to deal with a battery setup).

The battery must first be charged. The battery consists of a black and a red wire. The black wire will go to B- and the red wire will go to B+. The light will be blue if there is charging. **Do not let the black and red wires touch**. Once the battery is charged you can then connect it to the ESP32. The red wire goes to 5V and the black wire goes to GND. If this is working the light on the ESP32 should light up green, meaning there is power. 

## Arduino Setup

Once the physical hardware has been setup, we can move to the code. Clone this repository, then up on `input.ino` in Arduino. In the file you will see the following lines:
~~~C++
const char* ssid = "";
const char* password = "";
~~~
These two lines of code are used to connect to a WiFi network. `ssid` is the name of the network while `password` is the password for the network. You can also use your computer as a mobile hotstop and connect to it from there. Also important are the following lines:
~~~C++
pinMode(18, INPUT_PULLUP);
pinMode(32, INPUT_PULLUP);
~~~
Whatever ESP32 GPIO pins you chose to you for the buttons, make sure to put the pin number at the first parameter. Once the code has been compiled and uploaded, you should then open up the serial monitor and see an IP address printed. Take note of that IP address. 

## Python Setup

The file `art.py` handles the art creation. To create and run the visualizations, the Turtle module is used. This comes standard with most Python distributions. In the file, there is the following line:
~~~python
UDP_IP = "" # The IP that is printed in the serial monitor from the ESP32
~~~
Make sure to enter the IP address that is printed from the Arduino serial monitor once the ESP32 is connected. There is some additional setup that can be done to configure the display for you screen size.
~~~python
screen.setup(2000, 1000)
~~~
This code sets up the screen size, where the first parameter is the width and the second parameter is the height. Both measurements are in pixels. There is also the following lines:
~~~python
LEFT = -800
RIGHT = 800
TOP = 400
BOTTOM = -400
~~~
These variables set the dimension of the canvas, and are all in pixels. Adjust these values to get a canvas size that suites your needs. Once the `UDP_IP` address is entered, you can run the file and everything should run. Clicking the buttons changes the color used or the direction of the drawing. The threaing module is used so that one thread in running the Turtle graphics while another thread listens to the UDP socket. 
