class RAM:
   frames = []
   numFrames = 0
   maxFrames = 0
   bytesPerWord = 0
   
   def __init__(self, numFrames = 10, bytesPerWord = 4):
      self.frames = [] * numFrames
      self.numFrames = numFrames
      self.maxFrames = numFrames
      self.bytesPerWord = bytesPerWord

   def getFrame(self, frameNum):
      return self.frames[frameNum]

   def addFrame(self, frameNum, data):
      self.frames[frameNum] = data

   def get_data(self, frameNum, offset):
      byteStr = self.frames[frameNum]
      if (offset / self.bytesPerWord):
         return -1          #returns -1 if offset is not beginning of word
      else:
         return int(byteStr[offset : offset + self.bytesPerWord], 16)

      

