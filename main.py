from functools import partial
from models.database import HashSum, safe_data, check_data
import argparse
import hashlib
import logging
from file_hash import file_hash_sum, parse_dir, files_hash_sum, stdin_hash_sum
from multiprocessing import Pool
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(levelname)s]:%(message)s")
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files",
        type=str,
        default=sys.stdin,
        help="files for hash calc",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        default="md5",
        help=f"hashing algorithms for files: "
        f'{", ".join(hashlib.algorithms_available)}',
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="safe result to db",
    )
    parser.add_argument(
        "-c", "--check", action="store_true", help="hash diff comparison"
    )
    args = parser.parse_args()

    if args.files is not sys.stdin:
        with Pool() as pool:
            files = parse_dir(args.files)
            logger.debug(
                f" [files_hash_sum] was called with: files - "
                f"[{files}], hash_algorithm - [{args.algorithm}]"
            )
            res = pool.map_async(
                partial(file_hash_sum, hash_algorithm=args.algorithm), files
            )
            hash_sum = files_hash_sum(res.get(), args.algorithm)
            if args.save:
                safe_data(HashSum, args.files, hash_sum)
            if args.check:
                check_result = check_data(HashSum, args.files, hash_sum)
                logger.info(f" [check_result] - {check_result}")
            logger.info(f" [hash_sum] - {hash_sum}")
            print(hash_sum, args.files)
    else:
        result = stdin_hash_sum(args.files, args.algorithm)
        print(result, "-")
