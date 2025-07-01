import hashlib


def get_md5(file_path):
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_md5(file_path1, file_path2):
    """比较两个文件的MD5值"""
    md5_1 = get_md5(file_path1)
    md5_2 = get_md5(file_path2)

    if md5_1 == md5_2:
        print("两个文件的MD5值相同.")
    else:
        print("两个文件的MD5值不同.")
        print(f"{file_path1} 的MD5: {md5_1}")
        print(f"{file_path2} 的MD5: {md5_2}")

file1 = 'test.txt'
file2 = 'received_output.txt'
compare_md5(file1, file2)
