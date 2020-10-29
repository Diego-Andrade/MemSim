class PageTable:

    def __init__(self):
        # Const
        total_frames = 256

        self.page_table = [(-1, 0)] * total_frames      # List of tuples where tuple is (frame, loaded)

    def get_frame(self, page):
        entry = self.page_table[page] 
        if entry[1] == 0:
            return -1

        return entry[0]

    def load_frame(self, page, frame):
        self.page_table[page] = (frame, 1)

    def unload_frame(self, frame):
        for i in range(len(self.page_table)):
            entry = self.page_table[i]
            if entry[0] == frame:
                self.page_table[i] = (entry[0], 0)

    def is_page_loaded(self, page):
        return self.page_table[1]

    # Return list of loaded frames
    def get_loaded_pages(self):
        lf = []

        for i in range(len(self.page_table)):
            if self.page_table[i][1] == 1:
                lf.append((i, self.page_table[i][0]))

        return lf