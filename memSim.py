import sys
from Pra_Algorithims import *
from TLB import TLB
from Phy_Mem import RAM
from backingstore import BackingStore
from pagetable import PageTable

class MemSim:

    def __init__(self, address_filename, num_frames, pra):
        # CONST
        PAGE_SIZE = 256
        BACKINGSTORE_FILENAME = "BACKING_STORE.bin"

        # Sys info
        self.addr_filename = address_filename
        self.num_frames = num_frames
        self.pra_name = pra

        # Modules
        self.tlb = TLB()
        self.page_table = PageTable()       # List of tuples where tuple is (frame, loaded)
        self.ram = RAM(num_frames)  
        self.back_store = BackingStore(BACKINGSTORE_FILENAME, PAGE_SIZE) 
        if (pra == "fifo"):
            self.pra = FIFO(self.num_frames)
        elif (pra == "lru"):
            self.pra = LRU(self.num_frames)
        else:
            self.pra = OPT()

        # Mem Calls
        self.addresses = []         # List of tuples of (page, offset)
        self.translate()

        # Analytics
        self.total_access = 0
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
                num_frame = self.page_table.get_frame(e[0])
                if num_frame == -1:
                    self.pagefaults += 1
                    num_frame = self.handle_pagefault(e[0])

            logical_add = (e[0] << 8) & e[1]    # could store add instead of rebuilding as well
            if (pra == "lru"):
                self.pra.recordUse(num_frame)
            data = self.ram.get_data(num_frame, e[1])
            frame = self.ram.getFrame(num_frame)
            print('{}, {}, {}, {}\n'.format(logical_add, data, num_frame, frame))

            total_access += 1

        print('Number of Translated Addresses = {}'.format(self.total_access))
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
        else:
            if (self.pra_name == "opt"):
                frame = self.pra.getVictim(self.page_table.get_loaded_pages, self.addresses[self.total_access+1:])
            else:
                frame = self.pra.getVictim()

        self.page_table.unload_frame(frame)
        self.ram.addFrame(frame, data)
        self.tlb.loadAddress(page, frame)
        self.page_table.load_frame(page, frame)        

        return frame

if __name__ == "__main__":
    filename = sys.argv[1]
    frames = 265                # Default
    pra = "fifo"                # Default

    if len(sys.argv) < 3:
        print("Not enough arguments")
        sys.exit()
    if len(sys.argv) == 3:    # Frames given
        frames = int(sys.argv[2])
    if len(sys.argv) >= 4:    # Frames and PRA given
        pra = sys.argv[3]
    
    memSim = MemSim(filename, frames, pra)
    memSim.start()

