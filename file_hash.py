# Standard library imports
import hashlib
import io
import os


def file_hash_sum(file_name: str, hash_algorithm: str) -> str:
    """
    The function takes a file and a hashing algorithm as arguments,
     returns the hash sum

    :rtype: str
    :param file_name: file for hash calculation
    :param hash_algorithm: hashing algorithms for a file
    :return: hash sum of the file
    """
    h = hashlib.new(hash_algorithm)
    with open(file_name, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def parse_dir(path: str) -> list:
    """
    parser for dirs
    :param path: directory path
    :return: list of files
    """
    res = []
    if os.path.isfile(path):
        res.append(path)

    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.exists(filepath):
                res.append(filepath)
    return res


def files_hash_sum(files_hash: list, hash_algorithm: str) -> str:
    """
    :param files_hash: file hash list
    :param hash_algorithm: hashing algorithms for a file
    :return: final hash sum of the files
    """
    h = hashlib.new(hash_algorithm)
    for file_hash in files_hash:
        h.update(file_hash.encode())
    return h.hexdigest()


def stdin_hash_sum(stdin: io.TextIOWrapper, hash_algorithm: str) -> str:
    """
    :param stdin: stdin TextIOWrapper
    :param hash_algorithm: hashing algorithms for stdin
    :return: hash sum of the stdin
    """
    h = hashlib.new(hash_algorithm)
    h.update(stdin.read().encode())
    return h.hexdigest()
