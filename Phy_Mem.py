class RAM:
   frames = []
   numFrames = 0
   maxFrames = 0
   bytesPerWord = 0
   
   def __init__(self, numFrames = 10, bytesPerWord = 4):
      self.frames = [None] * numFrames
      self.numFrames = 0
      self.maxFrames = numFrames
      self.bytesPerWord = bytesPerWord

   def getFrame(self, frameNum):
      return self.frames[frameNum]

   def addFrame(self, frameNum, data):
      self.frames[frameNum] = data

      if (self.numFrames < self.maxFrames):
         self.numFrames += 1          

   def get_data(self, frameNum, offset):
      hexStr = self.frames[frameNum]
      val = int(hexStr[(offset*2):(offset*2) + 2], 16)
      if (val > 127):
         val = (256-val) * -1
      return val

      

