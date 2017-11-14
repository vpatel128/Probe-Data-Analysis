from math import sin, cos, sqrt, degrees, radians, pi, atan, asin
from probe import Probe
from link import Link
from makemap import Map
import csv

class MapMatch(object):

  def main(self):
    map1 = Map('Partition6467LinkData.csv')
    self.links = map1.makemap()
    self.probefile = 'Partition6467ProbePoints.csv'
    self.csvop = ''
    self.probepoints = []
    self.getProbePoints()
    
	

  def getProbePoints(self):
    print 'This will take time....'
    with open(self.probefile, 'r') as probe:
      i = 0
      readData = csv.reader(probe)
      MPoutputdata = open("Partition6467MatchedPoints.csv",'w'); MPoutputdata.close()
      SPoutputdata = open("SlopeOutput.csv",'w'); SPoutputdata.close()
      data = 'sampleID,  dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink'
      MPoutputdata = open("Partition6467MatchedPoints.csv",'a') 
      MPoutputdata.write(data+"\n");
      for data in readData:
        pdata = Probe(int(data[0]),str(data[1]),int(data[2]),float(data[3]),float(data[4]),\
          float(data[5]),float(data[6]),float(data[7]))
        if i == 0 :
          self.probepoints.append(pdata)
          i = i + 1
        elif self.probepoints[i-1].sampleID == pdata.sampleID :
          self.probepoints.append(pdata)
          i = i + 1
        else :
          self.probepoints = []
          self.probepoints.append(pdata)
          i = 1
        link = self.plotProbePoint(pdata)
        linkPVID = link.linkPVID
        distFromLink = link.perDistance(pdata)
        distFromRef = link.haversine(pdata)
        slope = self.slope(link,pdata)
        direction = link.directionOfTravel
        if direction == 'B':
            direction = 'X'
        data = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (pdata.sampleID, pdata.dateTime, pdata.sourceCode, pdata.latitude, pdata.longitude, pdata.altitude, pdata.speed, pdata.heading, linkPVID, direction, distFromRef, distFromLink)
	MPoutputdata.write(data+"\n");
        print str(pdata) + ' Link ID ' +str(linkPVID) + ','+ str(direction) + ','+str(distFromRef) + ','+str(distFromLink) + ',' + '\n' + slope + '\n'
      MPoutputdata.close();

  def plotProbePoint(self,pdata):
    mmlink = self.links.keys()[0]
    mindist = self.links[self.links.keys()[0]].perDistance(pdata)
    for link in self.links :
      perDistance = self.links[link].perDistance(pdata)
      if mindist > perDistance :
        mmlink = link
        mindist = perDistance
    return self.links[mmlink]

  def slope(self,link,pdata) :#calculating slope!!!!
    SPoutputdata = open("SlopeOutput.csv",'a')
    if len(self.probepoints) == 1 :
      return 'X'
    i = len(self.probepoints) - 2
    altitude = pdata.altitude - self.probepoints[i].altitude
    distance = self.haversine(pdata,self.probepoints[i])
    slope = altitude/distance
    if slope > 1 or slope < -1 :
      return 'Distance is very small between probes  : ' + str(distance) + 'm'
    derivedslope = degrees(asin(altitude/distance))
    if link.slopeInfo is None :
      linkPVID = link.linkPVID
      data = "%s, %s, %s" %(linkPVID, derivedslope, ' Surveyed slope : Not available ')
      SPoutputdata.write(data+"\n");
      SPoutputdata.close()
      return ' Derived slope : '+str(derivedslope)+' Surveyed slope : Not available '
    link1 = 0
    mindist = link.shapeDistance(pdata,link.geo[0],link.geo[1])    
    for i in range(1,len(link.slope)):
      slopedistance = link.shapeDistance(pdata,link.geo[i-1],link.geo[i])
      if slopedistance < mindist :
        link1 = i
        mindist = slopedistance
    error = float(link.slope[link1][1]) - derivedslope 
    linkPVID = link.linkPVID
    data = "%s, %s, %s" %(linkPVID, derivedslope, link.slope[link1][1])
    SPoutputdata.write(data+"\n");
    SPoutputdata.close()
    return ' Derived slope : '+str(derivedslope)+' Surveyed slope : '+str(link.slope[link1][1])+\
    ' error : '+ str(abs(error))


  def haversine(self,probepoint1,probepoint2):
   
    probepoint1.longitude, probepoint1.latitude, probepoint2.longitude, probepoint2.latitude = map(radians, [probepoint1.longitude, probepoint1.latitude , probepoint2.longitude, probepoint2.latitude])

    dlon = probepoint2.longitude - probepoint1.longitude 
    dlat = probepoint2.latitude - probepoint1.latitude 
    a = sin(dlat/2)**2 + cos(probepoint1.latitude) * cos(probepoint2.latitude) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371*1000 
    return c * r 

if __name__ == '__main__':
  MapMatch().main() 