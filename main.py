from time import sleep
from machine import Pin, PWM
import network
import socket
import time
import secret

#setting up wireless lan
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secret.ssid, secret.password)

#create the html in a variable
html = """<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Light Switch</title>
</head>

<body>
    <h2> light switch</h2>
    <a href="/on"><button>ON</button></a>
    <a href="/off"><button>OFF</button></a>
    <a href="/mid"><button>MID</button></a>

</body>

</html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
   
# Open socket
#gets the current ip address of the pi and declares port 80 as the port to work on
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


# Create a socket and make a HTTP request
s = socket.socket()
#this makes it so that the socket address can be reused
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(addr)
#declares how many devices can access this port
s.listen(1)

print("listening on", addr)

stateis = ""

# Listen for connections
while True:
    try:
        
        con, addr = s.accept()
        #this is the ip address of the device that connected to the pi
        print('client connected from', addr)
        #how many bytes to recieve
        request = con.recv(1024)
        print(request)

        request = str(request)
        #uses the /on and /off to know which one the user pressed
        
        light_on = request.find('/on')
        light_off = request.find('/off')
        light_mid = request.find('/mid')
        #when first opening the page on the server
        #the values are -1 bc it cannot find it since
        #no requests have been made
        print( 'light on = ' + str(light_on))
        print( 'light off = ' + str(light_off))
        print( 'light mid = ' + str(light_mid))
        #this while loop will always be running
        
        # if light_on == 6:
        #     pwm = PWM(Pin(1))
        #     pwm.freq(50)
        #     MAX = 1250000
        #     pwm.duty_ns(MAX)
            
                   
        # if light_off == 6:
        #     pwm = PWM(Pin(1))
        #     pwm.freq(50)
        #     MIN = 450000
        #     pwm.duty_ns(MIN)
            
        # if light_mid == 6:
        #     pwm = PWM(Pin(1))
        #     pwm.freq(50)
        #     MID = 600000
        #     pwm.duty_ns(MID)
        # Define constants for PWM duty cycles
PWM_FREQUENCY = 50
DUTY_CYCLE_MAX = 1250000
DUTY_CYCLE_MIN = 450000
DUTY_CYCLE_MID = 600000

# Initialize PWM on Pin 1
pwm = PWM(Pin(1))
pwm.freq(PWM_FREQUENCY)

def set_pwm_duty(light_status):
    if light_status == 'on':
        pwm.duty_ns(DUTY_CYCLE_MAX)
    elif light_status == 'off':
        pwm.duty_ns(DUTY_CYCLE_MIN)
    elif light_status == 'mid':
        pwm.duty_ns(DUTY_CYCLE_MID)
    else:
        raise ValueError("Invalid light_status. Use 'on', 'off', or 'mid'.")
            
           
         
        #sets the html
        response = html + stateis
        #sending the html page to the server so it can run it
        con.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        con.send(response)
        con.close()
 
    except OSError as e:
        con.close()
        print('connection closed')

