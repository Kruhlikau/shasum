# Standard library imports
import hashlib
import io
import os
import logging
from typing import Tuple, List

console_logger = logging.getLogger(__name__)
console_logger.setLevel(logging.INFO)
console_out = logging.StreamHandler()
console_logger.addHandler(console_out)


def file_hash_sum(file_name: str, hash_algorithm: str) -> Tuple[str, str]:
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
    return h.hexdigest(), file_name


def parse_dir(path: str) -> List[str]:
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


def stdin_hash_sum(stdin: io.TextIOWrapper, hash_algorithm: str) -> str:
    """
    :param stdin: stdin TextIOWrapper
    :param hash_algorithm: hashing algorithms for stdin
    :return: hash sum of the stdin
    """
    h = hashlib.new(hash_algorithm)
    h.update(stdin.read().encode())
    return h.hexdigest()


def print_res(data: List[Tuple[str, str]]) -> None:
    """
    :param data: list of tuples[hash_sum, file_path]
    :return: None
    """
    for hash_sum, file in data:
        console_logger.info(f"{hash_sum} {file}")


def check_path(file_path: str) -> str:
    """
    :param file_path: directory path
    :return: file_path.txt
    """
    if os.path.isfile(file_path):
        return f'{file_path.split("/")[-1].split(".")[0]}.txt'
    else:
        return f'{file_path.split("/")[-2]}.txt'
