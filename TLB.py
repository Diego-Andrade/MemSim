from Pra_Algorithims import FIFO


class TLB:

   def __init__(self, maxE = 16):
      self.pra = FIFO(maxE, [(None, None)])

   def checkAddress(self, pageNum):
      for i in self.pra.stack:
         if (i[0] == pageNum):
            return i[1]
      return -1 

   def loadAddress(self, pageNum, frameNum):
      if self.pra.numEntries < self.pra.maxEntries:
         self.pra.push([(pageNum, frameNum)])
         self.pra.numEntries += 1
      else:
         oldPage = -1
         for i in self.pra.numEntries:
            if i[1] == frameNum:
               oldPage = i[0]
         if oldPage != -1:
            self.pra.remove([(oldPage, frameNum)])
            self.pra.push([(pageNum, frameNum)])
         self.pra.getVictim(0)
         self.pra.push([(pageNum, frameNum)])
      
