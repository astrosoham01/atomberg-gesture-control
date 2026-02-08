# Gesture Controlled Atomberg Smart Fan

Control an Atomberg smart fan using hand gestures via computer vision.

## Features
- Hand gesture fan speed control
- Both hands gesture toggles LED
- Real-time local UDP control (no cloud delay)
- Works offline on same WiFi
- Built using Python + OpenCV + MediaPipe

## Tech Stack
Python  
OpenCV  
MediaPipe  
Socket UDP Networking  

## How it works
Camera detects hand gestures → Python processes fingers → Command sent to Atomberg fan locally over WiFi.

## Setup
Install dependencies:
pip install -r requirements.txt

Run:
python gesture_fan_control.py

## Demo
(Uploading demo video soon)
