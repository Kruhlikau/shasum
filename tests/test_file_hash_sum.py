# Related third party imports
import pytest

# Local imports
from file_hash import file_hash_sum


@pytest.mark.parametrize(
    "file_name, hash_algorithm, expected_result",
    [
        (
            "tests/test_data/test.txt",
            "md5",
            ("8dcfb1fe3591de419bae817d26c11d9f", "tests/test_data/test.txt"),
        ),
        (
            "tests/test_data/test.txt",
            "sha1",
            (
                "ba877c6918677766aa572472bf209fabcb90c798",
                "tests/test_data/test.txt",
            ),
        ),
        (
            "tests/test_data/test.txt",
            "whirlpool",
            (
                "0d4c8b5ad5e058d1941e"
                "7927ec4aa1b5f8d5de7b"
                "afc8d5cc0f36594c"
                "5322e4b9c44388e701788"
                "058dee2b4c149a47891824fa"
                "5558414049fa5e8dc5c04b338f9",
                "tests/test_data/test.txt",
            ),
        ),
    ],
)
def test_file_hash_sum_good(file_name, hash_algorithm, expected_result):
    assert file_hash_sum(file_name, hash_algorithm) == expected_result


@pytest.mark.parametrize(
    "expected_exception, file_name, hash_algorithm",
    [(TypeError, "test.txt", 5), (FileNotFoundError, "/tst.txt", "md5")],
)
def test_type_error(expected_exception, file_name, hash_algorithm):
    with pytest.raises(expected_exception):
        file_hash_sum(file_name, hash_algorithm)
