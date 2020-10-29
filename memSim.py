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

        self.pra_data = []      # List used page replacement algorithms FIFI and LRU

        # Mem Calls
        self.addresses = []         # List of tuples of (page, offset)
        self.translate()

    def translate(self):
        f_addr = open(self.addr_filename, "r")
        for line in f_addr:
            i_addr = int(line)
            page = i_addr >> 8
            offset = i_addr & 0xF
            self.addresses.append((page, offset))
        f_addr.close()
    
    def start(self):
        print(self.addresses)

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

