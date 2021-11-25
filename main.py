# Importing necessary libraries
from vpython import *
import math
from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk

# These globals will be important in order to create a dictionary containing
# all the planet objects
global planets
global number
global planetobjects
global modechoice
global currenttrack
currenttrack = 'planetsun'
number = 0
planets = {}
planetobjects = []
modechoice = 0

# Creating the planets for the 'regular' solar system mode
def initializeSolarSystem():
    global planetobjects
    sun = Planet("sun",0,0,0,0.15,0,333, 0,0,1000)
    mercury = Planet("mercury",0.387,0,0,0.009,1, 0.0553,0,1.59,0)
    venus = Planet("venus",0.723,0,0,0.025,1, 0.815,0,17.7,0)
    earth = Planet("earth", 1.2,0,0,0.034, 2, 1, 0, 17.1, 0)
    mars = Planet("mars", 1.52, 0, 0, 0.028, 1, 0.107, 0, 1.629, 0)
    jupiter = Planet("jupiter", 5, 0, 0, 0.1, 1, 10.8, 0, 87 ,0)
    # saturn = Planet("saturn", 0,-13, 0, 0.13, 1, 95.2, 400, 0 ,0)
    # uranus = Planet("uranus", 0,-15, 0, 0.08, 1, 14.5, 600, 0 ,0)
    # neptune = Planet("neptune", 0,-17, 0, 0.06, 1, 17.1, 800, 0 ,0)
    planetobjects = [sun, mercury, venus, earth, mars, jupiter]
    # Setting up the camera so that it follows the sun
    # through space instead of staying focussed on (0,0,0)
    scene.camera.follow(planets["planetsun"])
 
# Creating the environment suitable for the 'sandbox' mode   
def initializeSandbox():
    print("sandbox")
    pass


# This is the first thing the students will see when they open the program.
# The purpose of this method is to display a simple GUI for the students to
# interact with.
def welcome():
    class Application(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title('Solar System Simulation')                 # Creating the GUI window
            self.style = Style(theme='darkly')
            self.welcome = WelcomeScreen(self)
            self.welcome.pack(fill='both', expand='yes')
            
    # This class creates the content that is then applied to the above window.
    # The user is presented with two options, 'Regular' (Meaning a simulation of the
    # real solar system) or 'Sandbox' (Granting the user the ability to create their
    # own system).
    class WelcomeScreen(ttk.Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.configure(padding=(20,10))
            self.columnconfigure(2, weight=1)
            ttk.Label(master=self, text='Welcome to Python Solar System Simulation v0.1', width=35).grid(columnspan=4, pady=5)
            for i, label in enumerate(['Please Select Mode']):
                ttk.Label(master=self, text=label.title()).grid(row=i + 1, column=2, sticky='ew', pady=10, padx=(0, 10))
            self.regular = ttk.Button(master=self, text='Regular',command=self.regularmode).grid(row=4, column=1, sticky=tk.EW, pady=10, padx=(0, 10))
            self.sandbox = ttk.Button(master=self, text='Sandbox', command=self.sandboxmode).grid(row=4, column=3, sticky=tk.EW, pady=10, padx=(0, 3))
        
        def regularmode(self):
            self.quit()                   
                                            # The two methods connected to the two buttons 
        def sandboxmode(self):              # presented to the user. Depending on the choice  
            global modechoice               # either modechoice = 0 or modechoice = 1 will be returned.
            self.quit()
            modechoice = 1

    Application().mainloop()

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
                                                   mass = self.mass, make_trail = True, retain = 1000)
        
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
    GRAV = 1
    rvec = planet1.getPos() - planet2.getPos()
    rmag = mag(rvec)
    rhat = rvec/rmag
    forcemag = GRAV*((planet1.getMass()*planet2.getMass())/rmag**2)
    forcevec = -forcemag*rhat
    return forcevec

#                   CAMERA TRACK SWITCHING SYSTEM (DOESNT WORK)
def changetrack():
    global planets
    global currenttrack
    nexttrack = ''
    temp = list(planets.keys())
    for planet in temp:
        if currenttrack == planet:
            nexttrack = temp.index(planet)+1
    scene.camera.follow(planets[temp[nexttrack]])

# These 3 methods utilize an iterative approach to the physics equations
# behind the simulation in order to save many lines of repetetive code in the
# while loop found below.
dt = 0.00001
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
        if planet.getName() == 'sun':
            pass
        else:
            planet.updateMomentum(planet.getForce()*dt)
        
def updatePositions(planetobjects):
    for planet in planetobjects:
        if planet.getName() == 'sun':
            pass
        else:
            planet.updatePos(planet.getMomentum()/planet.getMass()*dt)


# The main loop that calls the above methods in order and therefore drives the simulation.
# the speed of the simulation can be adjusted within the rate() function. A higher value
# equates to a higher simulation speed.
def simulate():
    global currenttrack
    button(text='Switch Camera Track', pos=scene.title_anchor, bind=changetrack)
    dt = 0.0001
    t = 0
    while True:
        rate(10000)
        calcForces(planetobjects)
        updateMomenta(planetobjects)
        updatePositions(planetobjects)
        t += dt

def main():
    welcome()
    if modechoice == 0:
        initializeSolarSystem()
    elif modechoice == 1:
        initializeSandbox()
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
# - Make GUI close after selecting an option
 """