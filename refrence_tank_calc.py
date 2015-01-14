import math

# This script takes 4 paramaters describing an open top cylindrical tank, it dose a bit of math and tell you how much 
# force would be exurted on the very bottom bolt or rivet that is holding seam in the tank together, the shearing strength
# of the fastener would need to be about 3 times the shear force exurted on it to be cosiderd safe as a peachy printer tank 
# as it will have repeated loadings put on it. 


def centimetersFromInches(inches):
    return(inches*2.54)

def gramsFromPounds(pounds):
    return(pounds * 453.592)

# change these variables:

shearForceGoal = gramsFromPounds(30)
centimetersPerFastener = 1.3 # use cm This is the distance between the center hole of each fastener in your seam of your tank in the hight direction. 
circumference = centimetersFromInches(90.0) # use cm, the final cercumference of your tank ( after over laps of seams)
height = centimetersFromInches(96.0) # use cm, this is the Highes levle you will fill your tank to 
densityOfSatruatedSaltWater = 1.202 # use g/ml  or g/cubic-cm , this is for NaCl 
dollarsPerGramOfSalt =  5.0 / (20.0 * 1000.0) # use cad per gram .... ie  5 dolars / 20k grams 

minumumDistanceBetweenBolts = 2 #

def diameterFromCircumference(circumference):
    return(circumference / math.pi)

def radiusFromDiameter(diameter):
    return(diameter / 2.0)

def areaFromRadius(radius):
    return(math.pi * radius * radius)

def volumeFromRadiusAndHeight(radius, height):
    return(math.pi * radius * radius * height)

def weightFromVolumeAndDensity(volume, density):  #needs units
    return(volume * density)

def hoopAreaPerFastenerFromDiameterAndCentimetersPerFastener(diameter, centimetersPerFastener):
    return(diameter * centimetersPerFastener)

def volumeAboveHoopAreaPerFastenerFromHoopAreaPerFastenerAndHeight(hoopAreaPerFastener, height):
    return(hoopAreaPerFastener * height)

def wieghtOnHoopAreaFromVolumeAboveHoopAreaPerFastenerAndDensity(volumeAboveHoopAreaPerFastener, density):
    return(volumeAboveHoopAreaPerFastener * density)

def shearForceFromWeightOnHoopArea(weightOnHoopArea):
    return(weightOnHoopArea / 2.0)

def poundsFromGrams(grams):
    return(grams*.00220462)

def massOfSalt(weight):
    return(weight*.26)

def costOfSalt(massOfSalt, dollarsPerGramOfSalt):
    return(massOfSalt * dollarsPerGramOfSalt)


def boltsCapabilityAtHeight( height, diameter, density, shearForceGoal):
   
    forceOnOneCm = gPerSqCmAtHeight(density,height)*1*diameter
    BoltSeparation = shearForceGoal/(forceOnOneCm/2)

    return (BoltSeparation)

def gPerSqCmAtHeight(density,height):
    return(density*height)




diameter = diameterFromCircumference(circumference) # cm
radius = radiusFromDiameter(diameter) #cm
hoopAreaPerFastener = hoopAreaPerFastenerFromDiameterAndCentimetersPerFastener(diameter,centimetersPerFastener) #cm
area = areaFromRadius(radius) # cm squar
volume = volumeFromRadiusAndHeight(radius, height) # cm cubed == ml 
weight = weightFromVolumeAndDensity(volume, densityOfSatruatedSaltWater) # 1ml of water is 1 gram of weight
volumeAboveHoopAreaPerFastener = volumeAboveHoopAreaPerFastenerFromHoopAreaPerFastenerAndHeight(hoopAreaPerFastener, height) # cm qubed
weightOnHoopArea = wieghtOnHoopAreaFromVolumeAboveHoopAreaPerFastenerAndDensity(volumeAboveHoopAreaPerFastener, densityOfSatruatedSaltWater)  # retruns in grams 
shearForce = shearForceFromWeightOnHoopArea(weightOnHoopArea)  # return in grams
massOfSalt = massOfSalt(weight)
costOfSalt = costOfSalt(massOfSalt, dollarsPerGramOfSalt)
heightCoveredByBottomBolt = boltsCapabilityAtHeight( height, diameter, densityOfSatruatedSaltWater, shearForceGoal)

print ('%10.2f cm    circumference' % circumference)
print ('%10.2f cm    height' % height)
print ('%10.2f g/ml  density Of Satruated Salt Water' % densityOfSatruatedSaltWater)
print ('%10.2f cm    diameter' % diameter)
print ('%10.2f cm    radius' % radius)
print ('%10.2f cm^2  area' % area)
print ('%10.2f m^2   area' % (area / (100.0 * 100.0)))
print ('%10.2f l     volume' % (volume / 1000.0))
print ('%10.2f kg    weight' % (weight / 1000.0))
print ('%10.2f cm^2  hoop Area Per Fastener' % hoopAreaPerFastener)
print ('%10.2f cm^3  volume Above Hoop Area Per Fastener' % volumeAboveHoopAreaPerFastener)
print ('%10.2f kg    weight On Hoop Area' % (weightOnHoopArea / 1000.0))
print ('%10.2f kg    shear force' % (shearForce / 1000.0))
print ('%10.2f lbs   shear force' % poundsFromGrams(shearForce))
print ('%10.2f kg    mass Of Salt' % (massOfSalt / 1000.0))
print ('%10.2f $     cost of total salt needed to saturate full tank in dollars' % costOfSalt)

print ('height coverd by bottom bolt ', heightCoveredByBottomBolt)

print(' ')
print 'distance to next bolt starting at the bottom '

heightLeft = height
boltNumber = 0
distanceFromBottom = 0 

openSCadListOfBoltPlacements = []

while heightLeft > 0:
    boltNumber += 1 
    heightCoveredByBolt = boltsCapabilityAtHeight( heightLeft, diameter, densityOfSatruatedSaltWater, shearForceGoal)
    if heightCoveredByBolt > minumumDistanceBetweenBolts:
        heightCoveredByBolt = minumumDistanceBetweenBolts
    distanceFromBottom += heightCoveredByBolt
    print boltNumber, '  ', heightCoveredByBolt, '  ', distanceFromBottom
    openSCadListOfBoltPlacements.append(distanceFromBottom)
    heightLeft -= heightCoveredByBolt

print openSCadListOfBoltPlacements

print len(openSCadListOfBoltPlacements)
    



# some extra notes:

# ugg why int this open...  http://steelfinder.outokumpu.com/v3/StorageTank.aspx

#goals are shear per height 
#psi at at bottom 
#volume of water
#amout of salt needed. 

# http://moodlearn.ariel.ac.il/pluginfile.php/456055/mod_resource/content/0/pressure_vessels_1_.pdf
#http://en.wikipedia.org/wiki/Brine

# http://www.homedepot.ca/product/20-kg-crystal-plus-water-softener-salt/966409
