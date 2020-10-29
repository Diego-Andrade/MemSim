class PRA:

   def getVictim(self):
      raise NotImplementedError

class FIFO(PRA):
   stack = []
   
   def __init__(self, numFrames = 0):
      self.stack = [0] * numFrames
      for frame in range(numFrames):
         self.stack[frame] = frame

   def getVictim(self):
      frame = self.stack.pop(0)
      self.stack.append(frame)
      return frame

   def __repr__(self):
      return ''.join(str(e) for e in self.stack)

class LRU(PRA):
   stack = []

   def __init__(self, numFrames = 0):
      self.stack = []
      for frame in range(numFrames):
         self.stack.append(frame)

   def getVictim(self):
      frame = self.stack.pop(0)
      self.stack.append(frame)
      return frame

   def recordUse(self, frameNum):
      try:
         index = self.stack.index(frameNum)
         self.stack.pop(index)
         self.stack.append(frameNum)
      except ValueError:
         self.stack.append(frameNum)

   def __repr__(self):
      return ''.join(str(e) for e in self.stack)
