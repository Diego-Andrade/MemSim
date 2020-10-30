class PRA:

   def getVictim(self):
      raise NotImplementedError

   def recordUse(self):
      raise NotImplementedError

class FIFO(PRA):
   stack = []
   numEntries = 0
   maxEntries = 0
   
   def __init__(self, numFrames = 0, entry = None, fill = 1):
      self.stack = [entry] * numFrames
      self.numEntries = 0
      self.maxEntries = numFrames
      if fill == 1:
         for frame in range(numFrames):
            self.stack[frame] = frame
            self.numEntries += 1

   def getVictim(self, cycleVictim = 1):
      frame = self.stack.pop(0)
      if cycleVictim == 1:
         self.push(frame)
      else:
         self.numEntries -= 1
      return frame

   def recordUse(self, entry):
      try:
         index = self.stack.index(entry)
         self.stack.pop(index)
         self.stack.append(entry)
      except ValueError:
         print("FIFO.recordUse Failed")
         return

   def push(self, entry):
      self.stack.append(entry)
      self.numEntries -= 1

   def remove(self, entry):
      try:
         index = self.stack.index(entry)
         self.stack.pop(index)
         self.numEntries -= 1
      except ValueError:
         print("Nothing Cleared")
         return

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

class OPT(PRA):

   def getVictim(self, pages, addresses):
      frame = -1
      found_at = -1

      for e1 in pages:
         at = 0
         for e2 in addresses:
            if e1[0] == e2[0]:
               break
            at += 1
  
         if at >= found_at:           # > for selecting first if none or >= for selecting last
               found_at = at
               frame = e1[1]

      return frame

   def set_loaded_pages(self, pages):
      self.loaded_pages = pages