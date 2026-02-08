import socket
import json

FAN_IP = "********"   # your detected IP
PORT = 5600

command = {
    "speed": 0
}

message = json.dumps(command).encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (FAN_IP, PORT))
sock.close()

print("Speed command sent")
