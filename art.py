import turtle
from turtle import Screen
import random
from random import randint, randrange
import socket
import threading

# Create the UDP socket
UDP_IP = "" # The IP that is printed in the serial monitor from the ESP32
SHARED_UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.connect((UDP_IP, SHARED_UDP_PORT))

# Set screen size of display
screen = Screen()
screen.setup(2000, 1000)
turtle.title("Creative Random Art")

# Set dimension size
LEFT = -800
RIGHT = 800
TOP = 400
BOTTOM = -400
horizontals = [BOTTOM, TOP]
verticals = [LEFT, RIGHT]
colors = ["red", "yellow", "blue", "white"]
btn1 = "1"
color = random.choice(colors)

def x_pos():
    return randint(LEFT, RIGHT)

def y_pos():
    return randint(BOTTOM, TOP)

t = turtle.Turtle()

# Creates a rectangle starting from the bottom and moving up and then going right
def down_up_right():
    global t, verticals, horizontals, color
    t.color("black", color)
    t.begin_fill()
    start_x = x_pos()
    verticals.append(start_x)
    verticals.sort()
    vertical_index = verticals.index(start_x)

    start_index = randint(0, len(horizontals) - 2)
    start_y = horizontals[start_index]
    t.hideturtle()           
    t.penup()                
    t.goto(start_x, start_y)
    t.showturtle()           
    t.pendown()
    end_index = randint(start_index + 1, len(horizontals) - 1)
    end_y = horizontals[end_index]
    t.goto(start_x, end_y)


    if verticals[vertical_index + 1] == RIGHT:
        top_right = RIGHT
    else:
        idx = randint(vertical_index + 1, len(verticals) - 1)
        top_right = verticals[idx]
    
    t.goto(top_right, end_y)
    t.goto(top_right, start_y)
    t.goto(start_x, start_y)
    t.end_fill()

# Creates a rectangle starting from the bottom and moving up and then going left
def down_up_left():
    global t, verticals, horizontals, color
    t.color("black", color)
    t.begin_fill()
    start_x = x_pos()
    verticals.append(start_x)
    verticals.sort()
    vertical_index = verticals.index(start_x)

    start_index = randint(0, len(horizontals) - 2)
    start_y = horizontals[start_index]
    t.hideturtle()           
    t.penup()                
    t.goto(start_x, start_y)
    t.showturtle()           
    t.pendown()
    end_index = randint(start_index + 1, len(horizontals) - 1)
    end_y = horizontals[end_index]
    t.goto(start_x, end_y)


    if verticals[vertical_index - 1] == LEFT:
        top_right = LEFT
    else:
        idx = randint(0, vertical_index - 1)
        top_right = verticals[idx]
    
    t.goto(top_right, end_y)
    t.goto(top_right, start_y)
    t.goto(start_x, start_y)
    t.end_fill()

# Creates a rectangle that goes from the left to the right and then moves up
def left_right_up():
    global t, verticals, horizontals, color
    t.color("black", color)
    t.begin_fill()
    start_y = y_pos()
    horizontals.append(start_y)
    horizontals.sort()
    horizontal_index = horizontals.index(start_y)

    start_index = randint(0, len(verticals) - 2)
    start_x = verticals[start_index]
    t.hideturtle()           
    t.penup()                
    t.goto(start_x, start_y)
    t.showturtle()           
    t.pendown()
    
    end_index = randint(start_index + 1, len(verticals) - 1)
    end_x = verticals[end_index]
    t.goto(end_x, start_y)

    if horizontals[horizontal_index+ 1] == TOP:
        top_right = TOP
    else:
        idx = randint(horizontal_index + 1, len(horizontals) - 1)
        top_right = horizontals[idx]
    
    t.goto(end_x, top_right)
    t.goto(start_x, top_right)
    t.goto(start_x, start_y)
    t.end_fill()

# Creates a rectangle that goes from the left to the right and then moves down
def left_right_down():
    global t, verticals, horizontals, color
    t.color("black", color)
    t.begin_fill()
    start_y = y_pos()
    horizontals.append(start_y)
    horizontals.sort()
    horizontal_index = horizontals.index(start_y)

    start_index = randint(0, len(verticals) - 2)
    start_x = verticals[start_index]
    t.hideturtle()           
    t.penup()                
    t.goto(start_x, start_y)
    t.showturtle()           
    t.pendown()
    
    end_index = randint(start_index + 1, len(verticals) - 1)
    end_x = verticals[end_index]
    t.goto(end_x, start_y)

    if horizontals[horizontal_index - 1] == BOTTOM:
        top_right = BOTTOM
    else:
        idx = randint(0, horizontal_index - 1)
        top_right = horizontals[idx]
    
    t.goto(end_x, top_right)
    t.goto(start_x, top_right)
    t.goto(start_x, start_y)
    t.end_fill()

moves = [left_right_down, down_up_left, left_right_up, down_up_right]
move = random.choice(moves)

# Listens to the UDP socket for all incoming data
def collecting():
    global color, moves, move
    while True:
        data = sock.recv(2048).decode()
        print(data)
        if data[0] == '0':
            color = random.choice(colors)
        if data[1] == '0':
            move = random.choice(moves)

sock.send('Hello ESP32'.encode())
thread = threading.Thread(target=collecting)
thread.daemon = True
thread.start()


# Creating Iniital Frame
t.speed(6)
t.hideturtle()           
t.penup()                
t.goto(LEFT, TOP)
t.showturtle()           
t.pendown()
t.width(3)
t.goto(RIGHT, TOP)
t.goto(RIGHT, BOTTOM)
t.goto(LEFT, BOTTOM)
t.goto(LEFT, TOP)

while True:
    move()   

turtle.done() 