import sys
from TLB import TLB
from Phy_Mem import RAM
from backingstore import BackingStore

class MemSim:

    def __init__(self, address_filename, num_frames, pra):
        # CONST
        PAGE_SIZE = 256
        BACKINGSTORE_FILENAME = "BACKING_STORE.bin"

        # Sys info
        self.addr_filename = address_filename
        self.num_frames = num_frames
        self.pra = pra

        # Modules
        self.tlb = TLB()
        self.page_table = [(-1, 0)] * num_frames       # List of tuples where tuple is (frame, loaded)
        self.ram = RAM(num_frames)  
        self.back_store = BackingStore(BACKINGSTORE_FILENAME, PAGE_SIZE) 

        self.pra_stack = []      # List used page replacement algorithms FIFI and LRU

        # Mem Calls
        self.addresses = []         # List of tuples of (page, offset)
        self.translate()

        # Analytics
        self.pagefaults = 0
        self.tlb_misses = 0
        self.tlb_hits = 0

    def translate(self):
        f_addr = open(self.addr_filename, "r")
        for line in f_addr:
            i_addr = int(line)
            page = i_addr >> 8
            offset = i_addr & 0xFF
            self.addresses.append((page, offset))
        f_addr.close()
    
    def start(self):
        for e in self.addresses:    # e = (page, offset)
            num_frame = self.tlb.checkAddress(e[0])
            if num_frame != -1:
                self.tlb_hits += 1
            else:
                self.tlb_misses += 1
                num_frame = self.get_frame_from_page_table(e[0])
                if num_frame == -1:
                    self.pagefaults += 1
                    num_frame = self.handle_pagefault(e[0])

            logical_add = (e[0] << 8) & e[1]    # could store add instead of rebuilding as well
            data = self.ram.get_data(num_frame, e[1])
            frame = self.ram.getFrame(num_frame)
            print('{}, {}, {}, {}\n'.format(logical_add, data, num_frame, frame))

        print('Number of Translated Addresses = {}'.format(len(self.addresses)))
        print('Page Faults = {}'.format(self.pagefaults))
        print('Page Fault Rate = {}'.format(self.pagefaults / len(self.addresses)))
        print('TLB Hits = {}'.format(self.tlb_hits))
        print('TLB Misses = {}'.format(self.tlb_misses))
        print('TLB Hit Rate = {}'.format(self.tlb_hits / (self.tlb_hits + self.tlb_misses)))

    def handle_pagefault(self, page):
        data = self.back_store.get_page(page)
        frame = 0
        if (self.ram.numFrames < self.ram.maxFrames):
            frame = self.ram.numFrames                      # Using numFrames as index
        elif self.pra is 'fifo':
            frame = self.fifo(page)
        elif self.pra is 'lru':
            frame = self.lru(page)
        else:
            frame = self.opt(page)

        self.unload_frame_from_page_table(frame)
        self.ram.addFrame(frame, data)
        self.tlb.loadAddress(page, frame)
        self.load_frame_in_page_table(page, frame)        

        return frame

    def fifo(self, page):
        return 0

    def lru(self, page):
        return 0

    def opt(self, page):
        return 0

    def get_frame_from_page_table(self, page):
        entry = self.page_table[page] 
        if entry[1] == 0:
            return -1

        return entry[0]

    def load_frame_in_page_table(self, page, frame):
        self.page_table[page] = (frame, 1)

    def unload_frame_from_page_table(self, frame):
        for i in range(len(self.page_table)):
            entry = self.page_table[i]
            if entry[0] == frame:
                self.page_table[i] = (entry[0], 0)

if __name__ == "__main__":
    filename = sys.argv[1]
    frames = 265                # Default
    pra = "fifo"                # Default

    if len(sys.argv) >= 3:    # Frames given
        frames = int(sys.argv[2])
    
    if len(sys.argv) == 4:    # Frames and PRA given
        pra = sys.argv[3]
    
    memSim = MemSim(filename, frames, pra)
    memSim.start()

