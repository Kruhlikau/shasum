from functools import partial

import argparse
import hashlib
import logging
from file_hash import file_hash_sum, parse_dir, files_hash_sum
from multiprocessing import Pool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(name)s]:[%(levelname)s]:%(message)s")
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=str, help="files for hash calc")
    parser.add_argument(
        "hash_algorithm",
        type=str,
        default="md5",
        help=f"hashing algorithms for a file: "
        f'{", ".join(hashlib.algorithms_available)}',
    )
    args = parser.parse_args()
    files = parse_dir(args.files)
    logger.debug(
        f" [files_hash_sum] was called with: files - "
        f"[{files}], hash_algorithm - [{args.hash_algorithm}]"
    )
    with Pool() as p:
        res = p.map_async(
            partial(file_hash_sum, hash_algorithm=args.hash_algorithm), files
        )
        files_hash = files_hash_sum(res.get(), args.hash_algorithm)
        logger.info(f" [hash_sum] - {files_hash}")
