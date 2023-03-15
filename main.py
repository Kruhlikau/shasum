# Standard library imports
import multiprocessing.pool
from functools import partial
import hashlib
import logging
import sys

# Local imports
from file_hash import (
    file_hashsum,
    FileHandler,
    console_logger,
    print_data,
)

from models.database import DataInteraction

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
            files = FileHandler(args.files).parse_dirs()
            logger.debug(
                f" [files_hash_sum] was called with: files - "
                f"[{files}], hash_algorithm - [{args.algorithm}]"
            )
            async_res: multiprocessing.pool.MapResult = pool.map_async(
                partial(file_hashsum, hash_alg=args.algorithm),
                files,
                callback=print_data if not args.check else None,
            )
            async_res.get()
            data_interaction = DataInteraction(
                file_path=args.files, data=async_res.get()
            )
            if args.save:
                data_interaction.save_data()
            if args.check:
                data_interaction.check_data()
        else:
            hash_sum = file_hashsum(args.files, args.algorithm)
            console_logger.info(f"{hash_sum} -")
        sys.exit(0)
