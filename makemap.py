from link import Link
import csv

class Map(object):
  def __init__(self, fname):
    self.file = fname
    self.links = {}
  
  def makemap(self) :
    with open(self.file, 'r') as r:
      readData = csv.reader(r)
      for data in readData:
        linkPVID = int(data[0])
        refNodeID = int(data[1])
        nrefNodeID = int(data[2])
        length = float(data[3])
        directionOfTravel = data[5]
        shapeInfo = data[14]
        slopeInfo = data[16]
        self.links[linkPVID] = Link(linkPVID,refNodeID,nrefNodeID,length,directionOfTravel,shapeInfo,slopeInfo)
    return self.links