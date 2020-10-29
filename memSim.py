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
        if (self.ram.numFrames < self.ram.maxFrames):
            self.ram.addFrame(self.ram.numFrames, data)
            self.ram.numFrames += 1
        else:
            if self.pra is 'fifo':
                return self.fifo(page)
        
            if self.pra is 'lru':
                return self.lru(page)
        
            return self.opt(page)

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

    def update_page_table(self, page, frame=None, loaded=1):
        old_entry = self.page_table[page]

        new_entry = None
        if frame is None:
            new_entry = (old_entry[0], loaded)
        else:
            new_entry = (frame, loaded)
        
        self.page_table[page] = new_entry


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

