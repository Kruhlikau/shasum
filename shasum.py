import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str, help="file for hash calculation")
parser.add_argument(
    "hash_algorithm",
    type=str,
    default="md5",
    help=f"hashing algorithms for a file: "
    f'{", ".join(hashlib.algorithms_available)}',
)
args = parser.parse_args()


def file_hash_sum(file_name: str, hash_algorithm: str) -> str:
    """
    The function takes a file and a hashing algorithm as arguments,
     returns the hash sum

    :rtype: str
    :param file_name: file for hash calculation
    :param hash_algorithm: hashing algorithms for a file:
    :return: hash sum of the file
    """
    with open(file_name, "rb") as f:
        h = hashlib.new(hash_algorithm)
        h.update(f.read())
    return h.hexdigest()


print(file_hash_sum(args.file_name, args.hash_algorithm))
