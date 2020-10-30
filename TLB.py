from Pra_Algorithims import FIFO


class TLB:

   def __init__(self, maxE = 16):
      self.pra = FIFO(maxE, 0)

   def checkAddress(self, pageNum):
      if self.pra.stack:
         for i in self.pra.stack:
            if (i[0] == pageNum):
               return i[1]
      return -1 

   def loadAddress(self, pageNum, frameNum):
      if self.pra.stack:
         oldPage = -1
         for i in self.pra.stack:
            if i[1] == frameNum:
               oldPage = i[0]
         if oldPage != -1:
            self.pra.remove( (oldPage, frameNum) )
            self.pra.push( (pageNum, frameNum) )
            return
      if self.pra.numEntries < self.pra.maxEntries:
         self.pra.push( (pageNum, frameNum) )
      else:
         self.pra.getVictim(0)
         self.pra.push( (pageNum, frameNum) )
      
