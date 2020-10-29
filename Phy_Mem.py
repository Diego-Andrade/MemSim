class RAM:
   frames = []
   numFrames = 0
   maxFrames = 0
   
   def __init__(self, numFrames = 10):
      self.frames = [] * numFrames
      self.numFrames = numFrames
      self.maxFrames = numFrames

   def getFrame(self, frameNum):
      return self.frames[frameNum]

   def addFrame(self, frameNum, data):
      if (self.numFrames < self.maxFrames):
         self.frames[self.numFrames] = data
         self.numFrames += 1
      else:
         self.frames[frameNum] = data

