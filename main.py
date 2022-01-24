# Importing necessary libraries
from vpython import *
import numpy as np
from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk
import random as r

# These globals will be important in order to create a dictionary containing
# all the planet objects
scene = canvas(align='left')
scene.autoscale = False
scene.width = '1000'
scene.height = '720'
galaxy = sphere(pos=vector(0,0,0), radius = 25, texture='https://i.imgur.com/2YLRldk.png', shininess = 0)
planetInformation = canvas(width=400, height=720, align='left')
planets = {}
planetobjects = []
modechoice = 0
currenttrack = ''

# Creating the planets for the 'regular' solar system mode
def initializeSolarSystem():
    global planetobjects
    scene.select()
    sun = Planet("sun",0,0,0,0.15, 0 ,333,0,0,1000, True, False)
    mercury = Planet("mercury",0,0,0.387,0.009, 1 ,0.0553,1.59,0,0, False, False)
    venus = Planet("venus",0,0,0.723,0.025, 2 ,0.815,17.7,0,0, False, False)
    earth = Planet("earth",0,0,1.2,0.034, 3 ,1,17.1,0,0, False, False)
    mars = Planet("mars",0,0,1.62,0.028, 4 ,0.8,11.6853,0,0, False, False)
    jupiter = Planet("jupiter",0,0,5,0.04, 5 ,10.4,87,0,0, False, False)
    thick = 0.001
    rad = 0.15
    twopac = 0.1
    saturnobjects = []
    saturnbody = sphere(pos=vector(0,0,0), radius=0.08)
    saturnobjects.append(saturnbody)
    inner = False
    for i in range(1,35):
        if i == 15:
            rad -= 0.01
            twopac = 0.2
            inner = True
        if inner == False:
            saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.001, 0.002)*i), thickness = thick, opacity = twopac))
        elif inner == True:
            saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.001, 0.0015)*i), thickness = thick, opacity = twopac))
    saturn = compoundPlanet("saturn",0,0,8.2,saturnobjects,10,60,0,0, 0, False, False)
    uranus = Planet("uranus",0,0,14,0.05, 7 ,1,5,0,0, False, False)
    neptune = Planet("neptune",0,0,21,0.04, 8 ,1.3, 5.5,0,0, False, False)
    planetobjects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    scene.camera.follow(planets["planetsun"])                       # Setting up the camera so that it follows the sun
    scene.lights = []                                               # through space instead of staying focussed on (0,0,0)
    local_light(pos=vector(0,0,0))
    planetInformation.camera.pos = vector(0,0,10)
    planetInformation.userspin = False
    planetInformation.userzoom = False
    planetInformation.select()
    text(scene=planetInformation, text='Change information by selecting a new planet', pos=vector(-13,27,-15))

# This function is called when the user presses the 'Place Planet' button which appears
# upon selection of the sandbox mode.
planetNames = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
def placePlanet():
    global num
    normVec = scene.camera.pos/mag(scene.camera.pos)
    distFromCamera = mag(scene.camera.pos) - mag(normVec)
    startVal = 1                                                    # This section of the function utilizes 3-Dimensional
    while distFromCamera > 2:                                       # vector maths and coordinate geometry to find the position
        startVal += 0.1                                             # just infront of the user's view
        planetPos = startVal*normVec
        distFromCamera = mag(scene.camera.pos) - mag(planetPos)
    try:
        currentName = planetNames[num]
        if num == 5:                                                # Exception for saturn (need to create rings)
            thick = 0.001
            rad = 0.15
            twopac = 0.1
            saturnobjects = []
            saturnbody = sphere(pos=vector(0,0,0), radius=0.08)
            saturnobjects.append(saturnbody)
            inner = False
            for i in range(1,35):
                if i == 15:
                    rad -= 0.01
                    twopac = 0.2
                    inner = True
                if inner == False:
                    saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.001, 0.002)*i), thickness = thick, opacity = twopac))
                elif inner == True:
                    saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.001, 0.0015)*i), thickness = thick, opacity = twopac))
            currentName = compoundPlanet(planetNames[num],planetPos.x,planetPos.y,planetPos.z,saturnobjects,10,60,0,0, 0, False, False)
        else:   
            currentName = Planet(planetNames[num],planetPos.x,planetPos.y,planetPos.z,0.09, num+1 ,1,1.59,0,0, False, True)
        planetobjects.append(currentName)
        num += 1
    except:
        print('Too close')

# Acts like an undo button in the sandbox mode. The user can click a button
# that calls this method and the last planet they placed will be removed ready
# for reposition.
def deletePlanet():
    global num
    if num > 0:
        planetobjects[len(planetobjects)-1].delete()
        planetobjects.pop()
        num -= 1
    else:
        pass

# The method that is called when the user clicks the 'Start Simulation' button.
# It updated the start variable so that the planet positions are finalized and
# the simulation begins. 
start = False
def startSim():
    global start
    start = True

def updateMass(mass):
    planetobjects[len(planetobjects)-1].setMass(mass.value)
 
# Creating the environment suitable for the 'sandbox' mode
num = 0
def initializeSandbox():
    global planetobjects
    placeButton = button(bind=placePlanet, text='Place Planet')
    deleteButton = button(bind=deletePlanet, text='Delete Planet')
    startSimulation = button(bind=startSim, text='Start Simulation')
    massSlider = slider(min = 0.001, max = 30, value = 1, length = 300, bind=updateMass, right=15)
    sun = Planet("sun",0,0,0,0.55, 0 ,333,0,0,1000, True, False)
    planetobjects.append(sun)
    scene.camera.follow(planets["planetsun"])
    scene.lights = []
    local_light(pos=vector(0,0,0))
    while start == False:
        pass
    else:
        placeButton.delete()
        deleteButton.delete()
        startSimulation.delete()
        massSlider.delete()
        return True


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
    def __init__(self,name, posx, posy, posz, radius, texturenum, mass, m1, m2, m3, emissive, trail):
        global planets
        textures = ['https://i.imgur.com/rhDIk6x.jpeg', 'https://i.imgur.com/Y9KABlp.png', 'https://i.imgur.com/MFGRSTV.jpg', 
                    'https://i.imgur.com/Klu4RHH.jpg', 'https://i.imgur.com/6OWHL0V.jpg', 'https://i.imgur.com/z0QGLr4.jpg', 
                    'https://i.imgur.com/ayz5Vrc.jpg', 'https://i.imgur.com/kin15B0.jpg', 'https://i.imgur.com/LvfbPVm.jpg']
        self.name = name
        self.posx, self.posy, self.posz = posx, posy, posz
        self.position = vector(posx,posy,posz)
        self.radius = radius 
        self.texture = textures[texturenum]
        self.mass = mass
        self.momentum = vector(m1,m2,m3)
        self.force = vector(0,0,0)
        self.emissive = emissive
        planets["planet{0}".format(name)] = sphere(pos=self.position, radius=self.radius, 
                                                texture = self.texture, momentum = self.momentum,
                                                mass = self.mass, make_trail = trail, retain = 50, emissive = self.emissive, shininess = False)
            
    def getMass(self):
        return planets[f"planet{self.name}"].mass
    
    def setMass(self, newMass):
        planets[f"planet{self.name}"].mass = newMass
    
    def getPos(self):
        return planets[f"planet{self.name}"].pos
    
    def updatePos(self, newpos):
        planets[f"planet{self.name}"].pos += newpos
        
    def getRadius(self):
        return self.radius
    
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
    
    def delete(self):
        planets[f"planet{self.name}"].visible = False
        del planets[f"planet{self.name}"]
    
# A child class of Planet. This exists to handle the planet Saturn, the way Saturn
# is created in this program involves multiple objects instead of just one sphere.
# This calls for use of the 'compound' object rather than the 'sphere' object in Vpython.
# However the standard 'Planet' class only constructs sphere objects, hence the need for
# the 'compoundPlanet' child class.
class compoundPlanet(Planet):
    def __init__(self, name, posx, posy, posz, objects, mass, m1, m2, m3, texture, emissive, trail):
        textures = ['https://i.imgur.com/ayz5Vrc.jpg']
        self.name = name
        self.posx, self.posy, self.posz = posx, posy, posz
        self.position = vector(posx,posy,posz)
        self.mass = mass
        self.momentum = vector(m1,m2,m3)
        self.force = vector(0,0,0)
        self.objects = objects
        self.texture = textures[texture]
        self.emissive = emissive
        planets["planet{0}".format(name)] = compound(self.objects, pos=self.position, momentum = self.momentum, 
                                                    mass = self.mass, texture=self.texture, make_trail = trail, retain = 1000, emissive = self.emissive, shininess = False)
        
    def getRadius(self):
        return 1

# The following two classes are also children of the Planet class. Their purpose is to
# act as a simplified version of its parent. These classes are used in the process of 
# displaying the currently tracked planet. This is useful because in the information window
# planets neither move nor vary in size. Creating a planet instance for this purpose would be
# unnecessary and confusing.
class displayPlanet(Planet):
    def __init__(self, textureNum):
        textures = ['https://i.imgur.com/rhDIk6x.jpeg', 'https://i.imgur.com/Y9KABlp.png', 'https://i.imgur.com/MFGRSTV.jpg', 
                    'https://i.imgur.com/Klu4RHH.jpg', 'https://i.imgur.com/6OWHL0V.jpg', 'https://i.imgur.com/z0QGLr4.jpg', 
                    'https://i.imgur.com/ayz5Vrc.jpg', 'https://i.imgur.com/kin15B0.jpg', 'https://i.imgur.com/LvfbPVm.jpg']
        self.displayTexture = textures[textureNum]
        self.displayedPlanet = sphere(pos=vector(0,0,0), radius=5, texture=self.displayTexture, shininess=False)
    
    def delete(self):
        self.displayedPlanet.visible = False
        del self.displayedPlanet
        
    def rotate(self, angle, axis):
        try:
            self.displayedPlanet.rotate(angle=angle, axis=axis)
        except:
            pass
        
class displayCompoundPlanet(compoundPlanet):
    def __init__(self, textureNum, objects):
        textures = ['https://i.imgur.com/ayz5Vrc.jpg']
        self.displayTexture = textures[textureNum]
        self.objects = objects
        self.displayedPlanet = compound(self.objects, pos=vector(0,0,0), radius=5, texture=self.displayTexture, axis=vector(0,0,0.2), shininess=False)
        
    def delete(self):
        self.displayedPlanet.visible = False
        del self.displayedPlanet
        
    def rotate(self, angle, axis):
        self.displayedPlanet.rotate(angle=angle, axis=axis)
        

# This method continously checks the distance of the camera from the center of
# whatever the camera is currently tracking. It then uses this information to 
# scale large sphere with the stars texture on it. The purpose of this process 
# is to combat the naturally occuring problem that arises when zooming too far 
# into a sphere (View becomes obstructed by a black sphere that isn't actually 
# there).
def cameracheck():
    global planets
    center = vector(0,0,0)
    for planet in planets:
        if currenttrack == planet:
            center = vector(planets[planet].pos)
            galaxy.pos = vector(planets[planet].pos)
    zoomA = mag(center - scene.camera.pos)
    zoomB = mag(center - scene.camera.pos) + 1.5
    for item in np.linspace(zoomA, zoomB, num=40):              # The use of numpy's linspace feature
        galaxy.radius = item                                    # allows for smoothed radius adjustment
 
# The gravitational force equation, takes in two planet objects and returns
# resultant force vector, taking into account the planet's mass and position
def orbitcalc(planet1, planet2):
    GRAV = 1
    rvec = planet1.getPos() - planet2.getPos()
    rmag = mag(rvec)
    rhat = rvec/rmag
    forcemag = GRAV*((planet1.getMass()*planet2.getMass())/rmag**2)
    forcevec = -forcemag*rhat
    return forcevec

# The method called by the drop down menu created in the simulate() function
# below. This method matches the user's selected planet with a list of the
# planet objects and selects the correct planet to attatch the camera to.
# It also handles the changing of the planet in the information window to the
# right of the simulation.
def changetrack(m):
    global planets
    global currenttrack
    global current
    global currentLabel
    global planetTitle
    temp = list(planets.keys())
    names = []
    for planet in temp:
        names.append(planet.replace("planet","").capitalize())
    for i in range (len(planets)):
        if i == m.index:
            currenttrack = temp[i]
            scene.camera.follow(planets[temp[i]])
            if modechoice == 0:
                if i == 6:
                    thick = 0.1
                    rad = 6
                    twopac = 0.1
                    saturnobjects = []
                    saturnbody = sphere(pos=vector(0,0,0), radius=4)
                    saturnobjects.append(saturnbody)
                    inner = False
                    for i in range(1,35):
                        if i == 15:
                            rad -= 0.4
                            twopac = 2
                            inner = True
                        if inner == False:
                            saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.1, 0.2)*i), thickness = thick, opacity = twopac))
                        elif inner == True:
                            saturnobjects.append(ring(pos=vector(0,0,0), axis=vector(0.4,1,0), radius = rad-(r.uniform(0.1, 0.15)*i), thickness = thick, opacity = twopac))
                    current.delete()
                    for obj in currentLabel:
                        obj.visible = False
                        del obj
                    current = displayCompoundPlanet(0,saturnobjects)
                    currentLabel.append(label(pos=vector(2,3.5,0), 
                                         text='1.4808 billion km from the Sun, \nit takes roughly 29 years to orbit it once', 
                                         xoffset=20, yoffset=90))
                    currentLabel.append(label(pos=vector(-2,-3.5,0), 
                                         text='Gas giant,\nmostly hydrogen and helium', 
                                         xoffset=-40, yoffset=-90))
                    currentLabel.append(label(pos=vector(2.75,-3,0), 
                                         text='Rings are only roughly\n10 metres thick', 
                                         xoffset=38, yoffset=-40))
                    currentLabel.append(label(pos=vector(-2.75,3,0), 
                                         text="Diameter of 116,460 km,\nover 9 times Earth's", 
                                         xoffset=-38, yoffset=40))
                    planetTitle.visible = False
                    del planetTitle
                    planetTitle = text(scene=planetInformation, text=names[6], pos=vector(-1,-27,-15))
                else:
                    # The lists that hold the facts that are displayed when a planet is selected
                    infos = [['Surface temperature of 5505°C,\nhottest at the core (roughly 15°C million)', "Accounts for 99.86"+'%'+" \nof the solar system's mass", "Over 1 million times\nthe size of Earth", "4.6 billion years old"],
                             ['Closest planet to the Sun\nat 49.154 million km', 'Diameter of 4,879.4 km\n(smallest in the solar system)', 'Surface temperature of 430°C', 'Orbits the Sun every 88 days'],
                             ['Takes longer to rotate on its axis\nthan to orbit the Sun', '108.2 million km from the Sun', 'Surface temperature of 475°C', 'Only planet in the solar system\nthat spins clockwise'],
                             ['70'+'%'+'of the surface is water', '149.6 million km from the Sun', 'Axis is tilted by 23.5°', 'Diameter of 12,742 km'],
                             ['227.9 million km from the Sun', 'Atmosphere is almost\nall Carbon Dioxide', 'Surface temperature of -60°C', 'Takes 687 days to orbit the Sun'],
                             ['Fastest spinning planet in the system\n(spins once every 11 hours)', '79 Moons, most well known:\nIo, Europa, Ganymede, Callisto', 'Surface temperature of -108°C', '746.51 million km from the Sun'],
                             [],
                             ['Most tilted planet in the solar system\n(tilt of 98°)','Coldest planet in the solar system\n(-195°C)','2.871 billion km from the Sun', 'Mostly hydrogen and helium'],
                             ['Most distant planet in the solar system\n(4.4747 billion km)', 'Smallest gas giant\nin the solar system (49,244 km)', 'Mostly hydrogen and helium', 'Takes 165 years to orbit the Sun']]
                    positions = [[vector(3,4,0),10,90],[vector(-3,-4.05,0),-20,-90],[vector(3.75,-3.28,0),35,-40],[vector(-3.75,3.4,0),-28,40]]
                    current.delete()
                    for obj in currentLabel:
                        obj.visible = False
                        del obj
                    current = displayPlanet(i)
                    planetTitle.visible = False
                    del planetTitle
                    planetTitle = text(scene=planetInformation, text=names[i], pos=vector(-1,-27,-15))
                    for j in range(4):
                        currentLabel.append(label(pos=positions[j][0], text=infos[i][j], xoffset=positions[j][1], yoffset=positions[j][2]))

# This handles the spinning animation of all planets, it takes into account the radius
# of the planet and spins it at an appropriate speed respective to that.            
def planetRotate(planets, planetobjects, current):
    if current == None:
        temp = list(planets.keys())
        for i in range (len(planets)):
            planets[temp[i]].rotate(angle=0.0006/((planetobjects[i].getRadius())), axis=vector(0,1,0))
    else:
        current.rotate(angle=0.0006/0.09, axis=vector(0,1,0))

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
    global planetobjects
    global planets
    global current
    global currentLabel
    global planetTitle
    names = []
    currentLabel = []
    for planet in planetobjects: 
        names.append(planet.getName().capitalize())
    if modechoice == 0:
        current = displayPlanet(0)
        currentLabel.append(label(pos=vector(0,0,0), text=names[0], xoffset=40, yoffset=90))
        planetTitle = text(scene=planetInformation, text='Sun', pos=vector(-1,-27,-15))
    menu(choices = names, pos = scene.title_anchor, bind=changetrack)
    dt = 0.0001
    t = 0
    count = 0
    while True:
        rate(4000)
        count += 1
        if count % 13 == 0:
            cameracheck()
        if count % 100 == 0:
            planetRotate(planets, planetobjects, None)
            if modechoice == 0:
                planetRotate(None, None, current)
        calcForces(planetobjects)
        updateMomenta(planetobjects)
        updatePositions(planetobjects)
        t += dt

# Calling methods in the correct order.
def main():
    welcome()
    if modechoice == 0:
        initializeSolarSystem()
        simulate()
    elif modechoice == 1:
        planetInformation.delete()
        scene.select()
        initializeSandbox()
        while start == False:
            pass
        else:
            simulate()

# Starts the program.
main()

""" 
# Notes/Targets:
#
# - Planet mass slider, Maybe size?
# - Fix 'Too close' error message so it is visible in the GUI
#
#   Maybe?
#       - Implement moon?
#           - moon = https://i.imgur.com/ux1dfdt.png
#       - Zoom speed limit?
#       - Fix orbits? Make them look more realistic
#       - Reset button
 """