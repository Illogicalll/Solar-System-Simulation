# Importing necessary libraries
from vpython import *
import math
#import tkinter as tk
#import keyboard

# These globals will be important in order to create a dictionary containing
# all the planet objects
global planets
global number
global planetobjects
number = 0
planets = {}
planetobjects = []

# Creating the planets
def initializeSolarSystem():
    """
    # Possible syntax?
    sun = Planet("sun",posx=0,posy=0,posz=0,radius=0.695,colour=0,mass=1000,m1=0,m2=0,m3=4000)
    mercury = Planet("mercury",posx=5.8,posy=0,posz=0,radius=0.00244,colour=1,mass=1,m1=0,m2=90,m3=0)
    """
    global planetobjects
    sun = Planet("sun",0,0,0,0.2,0, 1000, 0,0,4000)
    mercury = Planet("mercury",1,0,0,0.05,1, 1,0,30,0)
    venus = Planet("venus",0,3,0,0.075,1, 2,-35,0,0)
    earth = Planet("earth", 0,-4,0,0.1, 2, 10, 160, 0, 0)
    mars = Planet("mars", 0, 5.7, 0, 0.08, 1, 15, -190, 0, 0)
    jupiter = Planet("jupiter", 0,-8, 0, 0.1, 1, 100, 300, 0 ,0)
    saturn = Planet("saturn", 0,-13, 0, 0.13, 1, 100, 400, 0 ,0)
    uranus = Planet("uranus", 0,-15, 0, 0.08, 1, 80, 600, 0 ,0)
    neptune = Planet("neptune", 0,-17, 0, 0.06, 1, 50, 800, 0 ,0)
    planetobjects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    # Setting up the camera so that it follows the sun
    # through space instead of staying focussed on (0,0,0)
    scene.camera.follow(planets["planetsun"])



# This is the first thing the students will see when they open the program.
# The purpose of this method is to display a simple GUI for the students to
# interact with.
def welcome():
    pass

# The framework for constructing a planet, offers many tweakable variables from
# position to mass to momentum that the user can modify
class Planet(object):
    # Laying out the foundations
    def __init__(self,name, posx, posy, posz, radius, colour, mass, m1, m2, m3):
        global planets
        global number
        number += 1
        colours = [color.yellow, color.red, color.blue]
        self.name = name
        self.posx, self.posy, self.posz = posx, posy, posz
        self.position = vector(posx,posy,posz)
        self.radius = radius
        self.colour = colours[colour]
        self.mass = mass
        self.momentum = vector(m1,m2,m3)
        self.force = vector(0,0,0)
        planets["planet{0}".format(name)] = sphere(pos=self.position, radius=self.radius, 
                                                   color = self.colour, momentum = self.momentum, 
                                                   mass = self.mass, make_trail = True, retain = 100)
        
    def getMass(self):
        return planets[f"planet{self.name}"].mass
    
    def getPos(self):
        return planets[f"planet{self.name}"].pos
    
    def updatePos(self, newpos):
        planets[f"planet{self.name}"].pos += newpos
    
    def setForce(self, newforce):                      # These methods will be used later as a gateway into the class in order
        self.force = newforce                          # to update values that affect the orbits of the individual planets
        
    def getForce(self):
        return self.force
        
    def updateMomentum(self, newmomentum):
        planets[f"planet{self.name}"].momentum += newmomentum
        
    def getMomentum(self):
        return planets[f"planet{self.name}"].momentum
    
    def getName(self):
        return self.name
     
# The gravitational force equation, takes in two planet objects and returns the
# resultant force vector, taking into account the planet's mass and position
def orbitcalc(planet1, planet2):
    # GRAV = 6.67 * math.pow(10,-11)
    GRAV = 1
    rvec = planet1.getPos() - planet2.getPos()
    rmag = mag(rvec)
    rhat = rvec/rmag
    forcemag = GRAV*((planet1.getMass()*planet2.getMass())/rmag**2)
    forcevec = -forcemag*rhat
    return forcevec

""" 
#                   CAMERA TRACK SWITCHING SYSTEM (DOESNT WORK)
# planetnames = list(planets.keys())
# index = 0
# def changetrack(currenttrack):
#     for i, value in enumerate(planetnames):
#         if value == currenttrack:
#             index = i
#     try:
#         scene.camera.follow(planets[planetnames[index+1]])
#     except IndexError:
#         pass
# currenttrack = "planetsun"
# scene.camera.follow(planets[currenttrack])
# scene.bind('click keydown', changetrack(currenttrack)) 
 """

# These 3 methods utilize an iterative approach to the physics equations
# behind the simulation in order to save many lines of repetetive code in the
# while loop found below.
dt = 0
def calcForces(planetobjects):
    planetforce = vector(0,0,0)
    for planet in planetobjects:
        for otherplanet in planetobjects:
            if planet != otherplanet:
                planetforce += orbitcalc(planet, otherplanet)
            else:
                pass
        planet.setForce(planetforce)
        planetforce = vector(0,0,0)
        
def updateMomenta(planetobjects):
    for planet in planetobjects:
        planet.updateMomentum(planet.getForce()*dt)
        
def updatePositions(planetobjects):
    for planet in planetobjects:
        planet.updatePos(planet.getMomentum()/planet.getMass()*dt)


# The main loop that calls the above methods in order and therefore drives the simulation.
# the speed of the simulation can be adjusted within the rate() function. A higher value
# equates to a higher simulation speed.
def simulate():
    dt = 0.0001
    t = 0
    while True:
        rate(1000)
        calcForces(planetobjects)
        updateMomenta(planetobjects)
        updatePositions(planetobjects)
        t += dt

def main():
    welcome()
    initializeSolarSystem()
    simulate()

main()

""" 
# Notes:
# - Finish camera tracking switch system
# - Add remaining planets
#    - Fix orbits? Make them look more realistic
# - Replace basic colours with functional textures:
#    - earth = textures.earth
#    - moon = moontexture = 'https://thumbs.dreamstime.com/b/moon-surface-seamless-texture-background-closeup-moon-surface-texture-188679621.jpg'
# - Finish welcome screen (GUI)
 """