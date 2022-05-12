# Standard library imports
import hashlib
import os
import logging
from typing import Tuple, List, Union, Any

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

    def parse_dirs(self, file_path: str) -> List[str]:
        """
        :param file_path: file for hash calculation
        :return: Lists of files path
        """
        if os.path.isfile(file_path):
            self.res.append(file_path)
        else:
            for i in os.listdir(file_path):
                if "cache" in i or "git" in i:
                    continue
                # if '.git' in i:
                #     continue
                if ".idea" in i:
                    continue
                if ".DS_Store" in i:
                    continue
                new_path = os.path.join(file_path, i)
                if os.path.isdir(new_path):
                    self.parse_dirs(new_path)
                else:
                    self.res.append(new_path)

        return self.res

    def check_path(self) -> str:
        """
        :return: file_path.txt
        """
        if os.path.isfile(self.file_path):
            return f'{self.file_path.split("/")[-1].split(".")[0]}.txt'
        else:
            return f'{self.file_path.split("/")[-2]}.txt'
