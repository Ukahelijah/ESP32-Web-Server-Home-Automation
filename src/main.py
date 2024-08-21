import machine
import usocket as socket
import time
import network


timeout = 0 # WiFi Connection Timeout variable 

wifi = network.WLAN(network.STA_IF)

# Restarting WiFi
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

# fill in your wifi credentials
wifi.connect('SSID','Password') 

if not wifi.isconnected():
    print('connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)
        
if(wifi.isconnected()):
    print('Connected...')
    print('network config:', wifi.ifconfig())
    
# HTML Document

html='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body style="background-color: lightblue">
    <center>
        <form>
        <h2>IOT Home Automation Project with Micropython</h2>
        <h3>Television</h3>
        <button  name="Load1" value='ON' type='submit'  >ON</button>
        <button name="Load1" value='OFF' type='submit'>OFF</button>
        <h3>Room light</h3>
        <button name="Load2" value='ON' type='submit'>ON</button>
        <button name="Load2" value='OFF' type='submit'>OFF</button>
        <h3>kitchen light</h3>
        <button name="Load3" value='ON' type='submit'>ON</button>
        <button name="Load3" value='OFF' type='submit'>OFF</button>
        <h3>Air Conditioner</h3>
        <button name="Load4" value='ON' type='submit'>ON</button>
        <button name="Load4" value='OFF' type='submit'>OFF</button>
    </form>
    </center>
    
</body>
</html>
'''

# LOADs Pin Declaration 
TV = machine.Pin(15,machine.Pin.OUT)
TV.value(0)

Room = machine.Pin(2,machine.Pin.OUT)
Room.value(0)

Kitchen = machine.Pin(4,machine.Pin.OUT)
Kitchen.value(0)

AC = machine.Pin(22,machine.Pin.OUT)
AC.value(0)

# Initialising the Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = '' # Empty means, it will allow all IP address to connect
Port = 80 # HTTP port
s.bind(('',80)) # Host,Port

s.listen(5) # It will handle maximum 5 clients at a time

# main loop
while True:
  connection_socket,address=s.accept() # Storing Conn_socket & address of new client connected
  print("Got a connection from ", address)
  request=connection_socket.recv(1024) # Storing Response coming from client
  print("Content ", request) # Printing Response 
  request=str(request) # Coverting Bytes to String
  # Comparing & Finding Postion of word in String 
  TV_ON =request.find('/?Load1=ON')
  TV_OFF =request.find('/?Load1=OFF')
  
  Room_ON =request.find('/?Load2=ON')
  Room_OFF =request.find('/?Load2=OFF')
  
  Kitchen_ON =request.find('/?Load3=ON')
  kitchen_OFF =request.find('/?Load3=OFF')
  
  AC_ON =request.find('/?Load4=ON')
  AC_OFF =request.find('/?Load4=OFF')
  
  if(TV_ON==6):
    TV.value(1)   
  if(TV_OFF==6):
    TV.value(0)
    
  if(Room_ON==6):
    Room.value(1)   
  if(Room_OFF==6):
    Room .value(0)
    
  if(Kitchen_ON==6):
    Kitchen.value(1)   
  if(Kitchen_OFF==6):
    Kitchen.value(0)
    
  if(AC_ON==6):
    AC.value(1)   
  if(AC_OFF==6):
    AC.value(0)
    
  # Sending HTML document in response everytime to all connected clients  
  response=html 
  connection_socket.send(response)
  
  #Closing the socket
  connection_socket.close() 
  #mind you can increase the number of load
