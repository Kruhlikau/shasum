# Standard library imports
from functools import partial
import hashlib
import logging
import sys

# Local imports
from file_hash import file_hash_sum, parse_dir, stdin_hash_sum, print_res
from models.database import check_data, save_data

# Related third party imports
import argparse
from multiprocessing import Pool

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

    with Pool() as pool:
        if args.files is not sys.stdin:
            files = parse_dir(args.files)
            logger.debug(
                f" [files_hash_sum] was called with: files - "
                f"[{files}], hash_algorithm - [{args.algorithm}]"
            )
            async_res = pool.map_async(
                partial(file_hash_sum, hash_algorithm=args.algorithm),
                files,
                callback=print_res if not args.check else None,
            )
            async_res.get()
            if args.save:
                save_data(async_res.get(), file_path=args.files)
            if args.check:
                check_data(args.files, async_res.get())
            sys.exit(0)
        else:
            hash_sum = stdin_hash_sum(args.files, args.algorithm)
            print(hash_sum, "-")
            sys.exit(0)
