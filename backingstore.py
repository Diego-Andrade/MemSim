class BackingStore:

    def __init__(self, filename, page_size):
        self.filename = filename
        self.PAGE_SIZE = page_size

    def get_page(self, page):
        f_disk = open(self.filename, "rb")
        f_disk.seek(page * self.PAGE_SIZE, 0)

        strByte = ''
        for _ in range(self.PAGE_SIZE):
            byte = f_disk.read(1)
            strByte += byte.hex().upper()

        f_disk.close()

        return strByte


