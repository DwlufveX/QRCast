import os
import zlib

buffer = {}
output_file = "../received_output.txt"


def write_data(index, compressed_data):
    buffer[index] = zlib.decompress(compressed_data)


def get_size():
    return sum(len(chunk) for chunk in buffer.values())


def get_md5():
    if not buffer:
        return None
    import hashlib
    all_data = b''.join(buffer[k] for k in sorted(buffer))
    with open(output_file, 'wb') as f:
        f.write(all_data)
    return hashlib.md5(all_data).hexdigest()