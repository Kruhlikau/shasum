# Standard library imports
import hashlib
import os
import logging
from typing import Tuple, List, Union, Any

# Local imports
from config import exclude

console_logger = logging.getLogger(__name__)
console_logger.setLevel(logging.INFO)
console_out = logging.StreamHandler()
console_logger.addHandler(console_out)


def file_hashsum(file_name: Any, hash_alg: str) -> Union[Tuple[str, str], str]:
    """
    The function takes a file and a hashing algorithm as arguments,
     returns the hash sum
    :rtype: Union[Tuple[str, str], str]
    :param file_name: file/stdin for hash calculation
    :param hash_alg: hashing algorithms for a file
    :return: hash sum of the file/stdin
    """
    h = hashlib.new(hash_alg)
    if type(file_name) is str:
        with open(file_name, "rb") as f:
            h.update(f.read())
        return h.hexdigest(), file_name
    else:
        h.update(file_name.read().encode())
        return h.hexdigest()


def print_data(data: List[Tuple[str, str]]) -> None:
    """
    :param data: list of tuples[hash_sum, file_path]
    :return: None
    """
    for hash_sum, file in data:
        console_logger.info(f"{hash_sum} {file}")


class FileHandler:
    def __init__(self, file_path: str):
        self.res: List[str] = []
        self.file_path = file_path

    def parse_dirs(self) -> List[str]:
        """
        parser for dirs
        :return: list of files
        """
        res = []

        if os.path.isfile(self.file_path):
            res.append(self.file_path)

        for root, dirs, files in os.walk(self.file_path, topdown=True):
            for ex in exclude:
                if ex in dirs:
                    dirs.remove(ex)
            for name in files:
                filepath = os.path.join(root, name)
                if os.path.exists(filepath):
                    res.append(filepath)
        return res

    def check_path(self) -> str:
        """
        :return: file_path.txt
        """
        if os.path.isfile(self.file_path):
            return f'{self.file_path.split("/")[-1].split(".")[0]}.txt'

        elif os.path.isdir(self.file_path):
            return f'{self.file_path.split("/")[-2]}.txt'

        elif not os.path.exists(self.file_path):
            raise FileNotFoundError
        return ""
