import hashlib
import zlib

class FileHead:
    def __init__(self, md5: str, file_size: int):
        self.md5 = md5
        self.file_size = file_size

def read_head(file_path):
    h = hashlib.md5()
    size = 0
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            size += len(chunk)
            h.update(chunk)
    return FileHead(h.hexdigest(), size)

def read_pages(file_path, chunk_size=800):
    with open(file_path, "rb") as f:
        index = 0
        while chunk := f.read(chunk_size):
            compressed = zlib.compress(chunk)
            yield index, compressed
            index += 1
