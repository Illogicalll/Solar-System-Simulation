from vpython import *
import math

moontexture = 'https://thumbs.dreamstime.com/b/moon-surface-seamless-texture-background-closeup-moon-surface-texture-188679621.jpg'
suntexture = 'https://images-repo-resized.s3-eu-west-1.amazonaws.com/2020/05/20/f48f469bd71cd046d3e9cb340fb608ce_large.png'

def RealisticSolarSystem():
    sun = sphere(pos=vector(0,0,0), color = color.yellow, radius = 1)
    earth = sphere(pos=vector(-200,0,0), texture=textures.earth, radius = 0.06371, make_trail = true)
    earthv = vector(0,0,5)
    for i in range(1000):
        earth.pos = earth.pos + earthv
    #moon = sphere(pos=vector(10,2,10), texture='https://thumbs.dreamstime.com/b/moon-surface-seamless-texture-background-closeup-moon-surface-texture-188679621.jpg', radius = 0.017374)
    
    #slider = slider(bind=scene.caption_anchor) 

def ScaledSystem():
    ME = 5.973 * math.pow(10,24)
    MM = 7.347 * math.pow(10,22)
    MS = 1.989 * math.pow(10,30)
    MMER = 3.285 * math.pow(10,23)
    REM = 384400000
    RSE = 149600000000
    GRAV = 6.67 * math.pow(10,-11)
    FEM = GRAV*(ME*MM)/math.pow(REM,2)
    FES = GRAV*(MS*ME)/math.pow(RSE,2)
    wM = math.sqrt(FEM/(MM*REM))
    wE = math.sqrt(FES/(ME*RSE))
    thetazero = 0
    
    def posMoon(t):
        theta = thetazero+wM*t
        return theta

    def posEarth(t):
        theta = thetazero+wE*t
        return theta

    def fromDaystoS(d):
        s = d*24*60*60
        return s

    def fromStoDays(s):
        d = s/60/60/24
        return d

    def fromDaystoH(d):
        h = d*24
        return h

    days = 365
    seconds = fromDaystoS(days)
    v = vector(0.5,0,0)
    sun = sphere(pos=vector(0,0,0), color = color.yellow , radius = 1)
    mercury = sphere(pos=vector(1.5,0,0), radius=0.3, make_trail=True, retain = 30)
    earth = sphere(pos=vector(5,0,0), texture = textures.earth, radius = 0.3, make_trail = True, retain = 200)
    moon = sphere(pos=earth.pos+v, texture = moontexture, make_trail = True, retain = 25, radius = 0.1)

    t = 0
    dt = 5000
    mooncounter = 0

    while True:
        rate(40)
        thetaEarth = posEarth(t+dt) - posEarth(t)
        thetaMoon = (posMoon(t+dt) - posMoon(t))*10
        earth.pos = rotate(earth.pos, angle = thetaEarth, axis = vector(0,0,1))
        v = rotate(v, angle = thetaMoon, axis = vector(0,0,1))
        moon.pos = earth.pos + v
        if moon.pos.z == earth.pos.z:
            mooncounter += 1
        t += dt

    # earthv = vector(0,0,7)
    # moonv = vector(0,0,3)
    # while True:
    #     rate(100)
    #     earth.pos += earthv
    #     moon.pos += moonv
    #     dist = (earth.pos.x**2 + earth.pos.y**2 + earth.pos.z**2)**0.5
    #     distmoon = (moon.pos.x**2 + moon.pos.y**2 + moon.pos.z**2)**0.5
    #     RadialVector = (earth.pos - sun.pos)/dist
    #     RadialVectorMoon = (moon.pos - earth.pos)/distmoon
    #     Fgrav = -10000*RadialVector/dist**2
    #     Fgravmoon = -10000*RadialVectorMoon/distmoon**2
    #     earthv = earthv + Fgrav
    #     moonv = moonv + Fgravmoon
    #     earth.pos += earthv
    #     moon.pos += moonv
    #     if dist <= sun.radius: break
    #moon = sphere(pos=vector(10,2,10), texture='https://thumbs.dreamstime.com/b/moon-surface-seamless-texture-background-closeup-moon-surface-texture-188679621.jpg', radius = 0.017374)



valid = False

while valid == False:
    simSelection = int(input("Please enter either 1 or 2 to run the default solar system or create your own: "))
    if simSelection == 1:
        global GRAVITY
        GRAVITY = 0
        valid2 = False
        while valid2 == False:
            RealSelection = int(input("Would you like to use a scaled model (1) or use a realistic model (2)?: "))
            if RealSelection == 1:
                ScaledSystem()
                valid2 = True
            elif RealSelection == 2:
                RealisticSolarSystem()
                valid2 = True
            else:
                print("Invalid selection, please enter either 1 or 0")
        valid = True
    # elif simSelection == 2:
    #     global GRAVITY
    #     GRAVITY = float(input("Enter your gravity value: "))
    #     CustomSystem()
    #     valid = True
    else:
        print("Invalid selection, please enter either 1 or 2.")

# scene.range = 4
# box() # display a box for context

# def showSphere(evt):
#     loc = evt.pos
#     sphere(sphere(pos=loc, texture=textures.earth, radius = 6.371))

# scene.bind('click', showSphere)