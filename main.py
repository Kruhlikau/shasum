import argparse
import hashlib
import logging
from file_hash import file_hash_sum

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(name)s]:[%(levelname)s]:%(message)s")
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, help="file for hash calc")
    parser.add_argument(
        "hash_algorithm",
        type=str,
        default="md5",
        help=f"hashing algorithms for a file: "
        f'{", ".join(hashlib.algorithms_available)}',
    )
    args = parser.parse_args()
    logger.debug(
        f" [file_hash_sum] was called with: file_name - "
        f"[{args.file_name}], hash_algorithm - [{args.hash_algorithm}]"
    )
    res = file_hash_sum(args.file_name, args.hash_algorithm)
    logger.info(f" hash_sum - " f"{res}")
