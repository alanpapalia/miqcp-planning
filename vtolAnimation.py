import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
import vtolParam as P
from math import cos, sin

class rotatingObject(object):
    def __init__(self, ax):
        self.mpatch_obj = None
        self.ax = ax

    def rotate_obj(self, theta, x, y):
        ts = self.ax.transData
        coords = ts.transform([x, y])
        tr = mpl.transforms.Affine2D().rotate_around(coords[0], coords[1], theta)
        t = ts + tr
        self.mpatch_obj.set_transform(t)

class rotatingRectangle(rotatingObject):
    def __init__(self, ax, xc, yc, th, w, h, fc_color='red', ec_color='black'):
        super(rotatingRectangle, self).__init__(ax)
        self.w = w
        self.h = h
        xy_bl = (xc - self.w/2, yc - self.h/2)
        self.mpatch_obj = mpatches.Rectangle(xy_bl, self.w, self.h, fc=fc_color, ec=ec_color)
        self.rotate_obj(th, xc, yc)

    def transform(self, xc, yc, theta):
        xy_bl = (xc - self.w/2, yc - self.h/2)
        self.mpatch_obj.set_xy(xy_bl)
        self.rotate_obj(theta, xc, yc)

class rotatingEllipse(rotatingObject):
    def __init__(self, ax, xc, yc, th, w, h, fc_color='red', ec_color='black'):
        super(rotatingEllipse, self).__init__(ax)
        self.w = w
        self.h = h
        xy = (xc, yc)
        self.mpatch_obj = mpatches.Ellipse(xy, self.w, self.h, fc=fc_color, ec=ec_color)
        self.rotate_obj(th, xc, yc)

    def transform(self, xc, yc, theta):
        self.mpatch_obj.center = xc, yc
        self.rotate_obj(theta, xc, yc)

class vtolAnimation:
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
        self.padding = 0.5                    # be used to contain handles to the
                                              # patches and line objects.
        self.obstacles = []
        plt.axis([-self.padding, P.L+self.padding, -self.padding, P.L]) # Change the x,y axis limits

        plt.plot([0, P.L],[0,0],'b-')         # Draw a base line
        plt.xlabel('z')
        
    def addObstacles(self, obstacles):
        self.obstacles = obstacles

    def drawVtol(self, states):
        zv = states[0]
        h = states[1]
        theta = states[2]

        self.drawCopter(zv, h, theta)
        self.drawObstacles()
        #self.ax.axis('equal') # This will cause the image to not distort

        # After each function has been called, initialization is over.
        if self.flagInit == True:
            self.flagInit = False
            
    def drawObstacles(self):
        if self.flagInit == True:
            for obstacle in self.obstacles:
                w = obstacle[1][0] - obstacle[0][0]
                h = obstacle[1][1] - obstacle[0][1]
                self.handle.append(mpatches.Rectangle(obstacle[0], w, h, fc='green', ec='black'))
                self.ax.add_patch(self.handle[-1])

    def drawCopter(self, zv, h, theta):
        if self.flagInit == True:
            self.copterArm = rotatingRectangle(self.ax, zv, h, theta, 2*P.d, P.caw)
            self.handle.append(self.copterArm.mpatch_obj)
            self.ax.add_patch(self.handle[-1])

            self.copterBody = rotatingRectangle(self.ax, zv, h, theta, P.cbw, P.cbw)
            self.handle.append(self.copterBody.mpatch_obj)
            self.ax.add_patch(self.handle[-1])

            self.leftRotor = rotatingEllipse(self.ax, zv-P.d*cos(theta), h-P.d*sin(theta), theta, P.rw, P.rh, fc_color='white')
            self.handle.append(self.leftRotor.mpatch_obj)
            self.ax.add_patch(self.handle[-1])

            self.rightRotor = rotatingEllipse(self.ax, zv+P.d*cos(theta), h+P.d*sin(theta), theta, P.rw, P.rh, fc_color='white')
            self.handle.append(self.rightRotor.mpatch_obj)
            self.ax.add_patch(self.handle[-1])
        else:
            self.copterArm.transform(zv, h, theta)
            self.copterBody.transform(zv, h, theta)
            self.leftRotor.transform(zv-P.d*cos(theta), h-P.d*sin(theta), theta)
            self.rightRotor.transform(zv+P.d*cos(theta), h+P.d*sin(theta), theta)
