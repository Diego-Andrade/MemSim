class TLB:
   entries = []
   maxEntries = 0
   incrementor = 0

   def __init__(self, maxE = 16):
      self.entries = [(None, None)]*maxE
      self.maxEntries = maxE

   def checkAddress(self, pageNum):
      for i in self.entries:
         if (i[0] == pageNum):
            return i[1]
      return -1 

   def loadAddress(self, pageNum, frameNum):
      self.entries[self.incrementor] = (pageNum, frameNum)
      if (self.incrementor >= self.maxEntries):
         self.incrementor = 0
      else:
         self.incrementor += 1
