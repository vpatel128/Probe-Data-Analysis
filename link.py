from math import sin, cos, atan2, sqrt, degrees, radians, pi, asin
from geopy.distance import great_circle as distance
from geopy.point import Point
from probe import Probe

class Link(object):
  def __init__(self, linkPVID, refNodeID, nrefNodeID, length, directionOfTravel, shapeInfo, slopeInfo):
    self.linkPVID = linkPVID
    self.refNodeID = refNodeID
    self.nrefNodeID = nrefNodeID
    self.length = length
    self.directionOfTravel = directionOfTravel
    self.shapeInfo = shapeInfo
    self.slopeInfo = slopeInfo
    self.geo = []
    self.slope = []
    self.getshape()
    self.getslope()
    self.link = ''

  def getshape(self): 
    for dat in self.shapeInfo.split('|'):
      info = [0,0]
      info[0], info[1], elevation = dat.split('/')
      self.geo.append(info)
    self.rlatitude = float(self.geo[0][0])
    self.rlongitude = float(self.geo[0][1])
    l = len(self.geo)
    self.nrlatitude = float(self.geo[l-1][0])
    self.nrlongitude = float(self.geo[l-1][1])

  def getslope(self): 
    if not self.slopeInfo :
      self.slopeInfo = None
      return 
    for dat in self.slopeInfo.split('|') :
      info = [0,0]
      info[0], info[1] = dat.split('/')
      self.slope.append(info)
      
  def haversine(self,probe):
    Xlat = probe.latitude
    Xlon = probe.longitude
    Ylat = self.rlatitude
    Ylon = self.rlongitude
    # CONVERT TO RADIANS
    Xlon, Xlat, Ylon, Ylat = map(radians, [Xlon, Xlat, Ylon, Ylat])

    # HAVERSINE
    lon = Ylon - Xlon 
    lat = Ylat - Xlat 
    a = sin(lat/2)**2 + cos(Xlat) * cos(Ylat) * sin(lon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371*1000 # IN KM
    return c * r 

  def shapeDistance(self, probe, point1, point2):
    p = Point(probe.latitude,probe.longitude)
    Xlat  = radians(float(point1[0])) 
    Xlon  = radians(float(point1[1]))
    Ylat  = radians(float(point2[0]))
    Ylon  = radians(float(point2[1]))
    x = cos(Ylat) * cos(Ylon - Xlon)
    y = cos(Ylat) * sin(Ylon - Xlon)
    lat = atan2( \
        sin(Xlat) + sin(Ylat), \
        sqrt(((cos(Xlat) + x)**2 + y**2)) )
    lon = Xlon + atan2(y, cos(Xlat) + x)
    lon = (lon + 3*pi) % (2*pi) - pi
    mid = Point(latitude=degrees(lat), longitude=degrees(lon))
    return distance(mid, p).km * 1000


  def perDistance(self, probe):
    p = Point(probe.latitude,probe.longitude)
    Xlat = radians(self.rlatitude) 
    Xlon = radians(self.rlongitude)
    Ylat = radians(self.nrlatitude) 
    Ylon = radians(self.nrlongitude)
    x = cos(Ylat) * cos(Ylon - Xlon)
    y = cos(Ylat) * sin(Ylon - Xlon)
    lat = atan2( \
        sin(Xlat) + sin(Ylat), \
        sqrt(((cos(Xlat) + x)**2 + y**2)) )
    lon = Xlon + atan2(y, cos(Xlat) + x)
    lon = (lon + 3*pi) % (2*pi) - pi
    mid = Point(latitude=degrees(lat), longitude=degrees(lon))
    return distance(mid, p).km * 1000

  

  def __str__(self) :
    return 'PVID ' + str(self.linkPVID) + ' Ref ID :'+ str(self.refNodeID) + ' lat :' + str(self.rlatitude) + ' long :' + str(self.rlongitude) \
         + ' NRef ID :'+ str(self.nrefNodeID) + ' lat :' + str(self.nrlatitude) + ' long :' + str(self.nrlongitude)


  def getnrefNodeID(self):
  	return self.nrefNodeID

  def getrefNodeID(self):
  	return self.refNodeID
