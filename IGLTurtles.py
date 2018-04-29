import turtle
from random import random
from math import sqrt, atan, pi, cos, sin
    
def get_Dimen_Velo(RMS, min, max):
    '''Returns an x value from a distribution that resembles a Gaussian with standard deviation RMS.
    Result can be positive or negative, with mean 0.
    Results will be clipped at peak absolute value max.
    A min of zero is recommended, but if it is set higher, return will have absolute value of at least min.
    Current implementation prevents going more than 2.57 standard deviations out.
    RMS around 4.4 tends to return results with absolute value between 0.5 and 10.5, with smaller values more often.'''
    perctile = random()*100
    if perctile >= 50:
        sign = 1
        speedRank = perctile - 50
    else:
        sign = -1
        speedRank = 50 - perctile 
    if speedRank <= 25:
        speed = 0.675 * speedRank/25
    elif speedRank <= 40:
        speed = 0.675 + (1.282-0.675)*(speedRank-25)/15
    elif speedRank <= 45:
        speed = 1.282 + (1.645-1.282)*(speedRank-40)/5
    elif speedRank <= 47.5:
        speed = 1.645 + (1.96 - 1.645)*(speedRank-45)/2.5
    else:
        speed = 1.96 + (2.326-1.96)*(speedRank-47.5)/1.5
    speed = RMS * speed
    if speed > max:
        speed = max
    if speed < min:
        speed = min
    return speed*sign
    
def getDegAngle(x, y):
    '''Returns an angle in degrees corresponding to a ratio of horizontal component x and vertical component y.
    Unlike atan, can return values in all four quadrants.
    Returns a value between -180 and 180, with values between -180 and -90 corresponding to the 3rd quadrant.
    Will have zero division error if x and y are both 0.'''
    if x == 0:
        return pi/2 * abs(y)/y
    rad = atan(y/x) #This line always gives answer in the 1st or 4th quadrant
    if x <0:
        if y<=0:
            rad -= pi
        else:
            rad += pi 
    return 180/pi * rad 
    

def randStartX(width):
    return int(random()*width)
def randStartY(height):
    return int(random()*height)

def initializeTurtle(name, tcolor, fillColor, penSize, inWidth, inHeight):
    name.color(tcolor)
    name.up()
    name.speed(0)
    name.goto(randStartX(inWidth), randStartY(inHeight))
    name.down()
    name.fillcolor(fillColor)
    name.pensize(penSize)
    
def setStartVel(tname, RM, dimSpeedMin, dimSpeedMax, stSpeedMin, stSpeedMax):
    '''Gives turtle a random (not uniformly distributed) orientation and velocity with "average" speed RM
    Velocity in x and y are determined with calls to get_Dimen_Velo
    Speed will always be between stSpeedMin and stSpeedMax
    It is recommended to use dimSpeedMin of 0 and dimSpeedMax at or slightly above stSpeedMax'''
    tXSpeed = get_Dimen_Velo(RM, dimSpeedMin, dimSpeedMax)
    tYSpeed = get_Dimen_Velo(RM, dimSpeedMin, dimSpeedMax)
    tname.left(getDegAngle(tXSpeed,tYSpeed))
    tSpeedNo = sqrt(tXSpeed**2 + tYSpeed**2)
    if tSpeedNo > stSpeedMax:
        tname.speed(stSpeedMax)
    elif tSpeedNo < stSpeedMin:
        tname.speed(stSpeedMin)
    else:
        tname.speed(round(tSpeedNo))

def turtleHeadingQuad(tname):
    return tname.heading() // 90 + 1

def wallCollideDist(tname, width, height):
    '''returns a list containing distance until a collision with a wall
    second list item is which wall will be collided with
    1 = right; 2 = upper; 3 = left; 4 = lower'''
    headg = tname.heading()
    tx = tname.xcor()
    ty = tname.ycor()
    if headg % 90 == 0:
        if ((headg == 0) or (headg == 360)):
            return [(width-tx), 1]
        elif headg == 90:
            return [(height - ty), 2]
        elif headg == 180:
            return [(tx - width), 3]
        else:
            return [(ty - height), 4]
    if turtleHeadingQuad(tname)==1:
        xCollDist = (width - tx) / cos(headg*pi/180)
        yCollDist = (height - ty) / sin(headg*pi/180)
        if xCollDist < yCollDist:
           wall = 1
        else:
            wall = 2
    elif turtleHeadingQuad(tname)==2:
        xCollDist = tx / abs(cos(headg*pi/180))
        yCollDist = (height - ty) / sin(headg*pi/180)
        if xCollDist < yCollDist:
            wall = 3
        else:
            wall = 2
    elif turtleHeadingQuad(tname)==3:
        xCollDist = tx / abs(cos(headg*pi/180))
        yCollDist = ty / abs(sin(headg*pi/180))
        if xCollDist < yCollDist:
            wall = 3
        else:
            wall = 4
    else:
        xCollDist = (width - tx) / cos(headg*pi/180)
        yCollDist = ty / abs(sin(headg*pi/180))
        if xCollDist < yCollDist:
            wall = 1
        else:
            wall = 4
    if xCollDist < yCollDist:
        return [xCollDist, wall]
    else:
        return [yCollDist, wall]

def wallBounce(tname, wall, hQuad=0):
    '''Makes a turtle bounce off a wall.
    Takes the turtle name, wall number and (optional) the quadrant of the turtle's heading'''
    thead = tname.heading()
    if hQuad==0:
        hQuad = min(tname.heading()//90 + 1, 4)
    if wall == 1:
        if hQuad == 1:
            tname.setheading(180 - thead)
        elif hQuad == 4:
            tname.setheading(270 - (thead - 270))
    elif wall == 2:
        if hQuad == 1:
            tname.setheading(360 - thead)
        elif hQuad == 2:
            tname.setheading(270 - (thead - 90))
    elif wall == 3:
        if hQuad == 2:
            tname.setheading(180 - thead)
        elif hQuad == 3:
            tname.setheading(360 - (thead - 180))
    else:
        if hQuad == 3:
            tname.setheading(90 + 270 - thead)
        elif hQuad == 4:
            tname.setheading(360 - thead)

def collideCheck(turt1, turt2):
    if turt1.xcor() == turt2.xcor():
        if turt1.ycor() == turt2.ycor():
            return True
    else:
        return False

def main():
    border = 10
    winWidthIn = 40*8
    winHeightIn = 360
    turtleStartVert = 100
    pensize = 3

    wn = turtle.Screen()             # Set up the window and its attributes
    wn.setworldcoordinates(0-border, 0-border, winWidthIn + border, winHeightIn + border)
    wn.bgcolor("lightgreen")

    turtle_list = []

    if ((not('tess' in locals())) and not('tess' in globals())):
        tess = turtle.Turtle()
        initializeTurtle(tess, "blue", "red", pensize, winWidthIn, winHeightIn)
    turtle_list.append(tess)

    if (not('mike' in locals())): # and not('mike' in globals())):
        mike = turtle.Turtle()
        initializeTurtle(mike, "blue", "red", pensize, winWidthIn, winHeightIn)
    turtle_list.append(mike)
    
    RMSpeed = 4.4
    '''tessXSpeed = get_Dimen_Velo(RMSpeed, 0, 11)
    tessYSpeed = get_Dimen_Velo(RMSpeed, 0, 11)
    tess.left(getDegAngle(tessXSpeed,tessYSpeed))
    tessSpeedNo = sqrt(tessXSpeed**2 + tessYSpeed**2)
    if tessSpeedNo > 10:
        tess.speed(10)
    elif tessSpeedNo < 1:
        tess.speed(1)
    else:
        tess.speed(round(tessSpeedNo))'''
    setStartVel(tess, RMSpeed, 0, 11, 1, 10)
    setStartVel(mike, RMSpeed, 0, 11, 1, 10)
    print(tess.speed())
    print(tess.heading())
    print(tess.xcor())
    print(tess.ycor())

    bouncecount = 10

    tessStop = wallCollideDist(tess, winWidthIn, winHeightIn)
    print(tessStop)
    mikeStop = wallCollideDist(mike, winWidthIn, winHeightIn)
    print(mikeStop)
    distList = [tessStop[0], mikeStop[0]] # Turtles in same order as turtle_list
    wallList = [tessStop[1], mikeStop[1]]
    collideTimeList = [distList[0]/tess.speed(), distList[1]/mike.speed()]
    
    for i in range(bouncecount):
        if (('collideHappened' in locals()) and collideHappened == 1):
            break
        shortestTime = min(collideTimeList)
        firstTurt = turtle_list[collideTimeList.index(shortestTime)]
        for j in range(int(shortestTime)):
            tess.forward(tess.speed())
            mike.forward(mike.speed())
            if collideCheck(tess, mike) == True:
                collideHappened = 1
                break
        wallBounce(firstTurt, wallList[collideTimeList.index(shortestTime)])
        for j in range(len(collideTimeList)):
            collideTimeList[j] -= shortestTime # may also want to update distList
        bounced_new_nextWallHit = wallCollideDist(firstTurt, winWidthIn, winHeightIn)
        collideTimeList[turtle_list.index(firstTurt)] = bounced_new_nextWallHit[0]/firstTurt.speed()
        wallList[turtle_list.index(firstTurt)] = bounced_new_nextWallHit[1]

    wn.exitonclick()

if __name__ == "__main__":
    main()

