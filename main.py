#Created for Professor Jennifer Cohen by (yumaikas) Andrew Owen to Python 2.7
# Adapted for Python 3 by Saulo Catharino | saulocatharino@gmail.com
#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from Tkinter import Tk, Canvas
except:
    from tkinter import Tk, Canvas
from math import sin, cos, radians
from datetime import datetime

class point():
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return point(x, y)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return point(x, y)
    def __str__(self):
        return '[x:{0}, y:{1}]'.format(self.x,self.y)
    def offsetByVector(self, angle, length):

        x = int(cos(angle) * length) + self.x
        y = int(sin(angle) * length) + self.y
        return point(x, y)

class clockHands():
    root = Tk()
    longHand = ""
    shortHand = ""
    secondHand = ""

    corner1 = point(10, 10)
    corner2 = point(210, 210)

    
    def centerPoint(self):

        x = (self.corner1.x + self.corner2.x)/2
        y = (self.corner1.y + self.corner2.y)/2
        return point(x, y)
    
    
    def updateClock(self, canvas):

        def initHand(hand, color, width):
            if hand == "":
                hand = canvas.create_line(0,0,0,0,\
                    fill = color, width = width, capstyle = "round")
                canvas.pack()
            return hand

        shortHand = self.shortHand = initHand(self.shortHand, "grey", 2)
        longHand = self.longHand = initHand(self.longHand, "black", 4)
        secHand = self.secondHand = initHand(self.secondHand, "red", 1)
        time = datetime.now()


        hourAngle = ((time.hour * 30.0) + (30.0 * (time.minute/60.0)))
        minuteAngle = ((time.minute * 6.0) + (6.0 * (time.second/60.0)))
        secondAngle = (time.second * 6)

        def drawHand(Hand, angle, length):

            angle -= 90.0
            
            rads = radians(angle)
            center = self.centerPoint()
            endPoint = center.offsetByVector(rads, length)
            canvas.coords(Hand, center.x, center.y, endPoint.x, endPoint.y)

        drawHand(longHand, hourAngle, 50)
        drawHand(shortHand, minuteAngle, 80)
        drawHand(secHand, secondAngle, 90)
        rotate = lambda: self.updateClock(canvas)
        canvas.after(100, rotate)
        
    def run(self):

        self.root.mainloop()

    def __init__(self):
        canvas = Canvas(self.root, width=220, height=220)
        

        corner1 = self.corner1
        corner2 = self.corner2
        
        canvas.create_oval(corner1.x, corner1.y, corner2.x, corner2.y,\
                           fill = "white", width = 3)
        center = self.centerPoint()

        def createTickMark(angle, dFromCenter, length, mark):
            angle -= 90.0
            rads = radians(angle)
            p1 = center.offsetByVector(rads, dFromCenter)
            p2 = center.offsetByVector(rads, dFromCenter + length)
            mark(p1, p2)

        sm_Tick = lambda p1, p2: canvas.create_line(p1.x, p1.y, p2.x, p2.y)
        lg_Tick = lambda p1, p2: canvas.create_line(p1.x, p1.y, p2.x, p2.y,\
                                                    fill = 'red', width=3)

        for angle in range(0, 360, 6):
            createTickMark(angle, 90, 9, sm_Tick)

        for angle in range(0, 360, 30):
            createTickMark(angle, 80, 19, lg_Tick)

        for angle in range(0, 360, 90):
            createTickMark(angle, 60, 10, sm_Tick)

        canvas.pack()
        self.root.wm_title("Relógio Analógico")

        self.updateClock(canvas)
        
def main():
    Hand = clockHands()
    Hand.run()
main()
