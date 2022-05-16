# Related third party imports
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Local imports
from models.database import HashSum

from file_hash import file_hashsum, print_data, FileHandler


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
    assert file_hashsum(file_name, hash_algorithm) == expected_result


@pytest.mark.parametrize(
    "expected_exception, file_name, hash_algorithm",
    [(TypeError, "test.txt", 5), (FileNotFoundError, "/tst.txt", "md5")],
)
def test_type_error(expected_exception, file_name, hash_algorithm):
    with pytest.raises(expected_exception):
        file_hashsum(file_name, hash_algorithm)


@pytest.mark.parametrize(
    "failed_data, expected_exception",
    [(5, TypeError), ([1, 2, 3], TypeError), ({1, 2, 3}, TypeError)],
)
def test_print_data(failed_data, expected_exception):
    with pytest.raises(expected_exception):
        print_data(failed_data)


@pytest.mark.parametrize(
    "file_path, expected_result",
    [
        (
            "tests/test_data/",
            ["tests/test_data/test.txt"],
        ),
        (
            "tests/test_data/test.txt",
            ["tests/test_data/test.txt"],
        ),
    ],
)
def test_parse_dirs(file_path, expected_result):
    assert FileHandler(file_path).parse_dirs() == expected_result
    assert FileHandler(file_path).parse_dirs() != []


@pytest.mark.parametrize(
    "expected_exception, file_path", [(TypeError, 123), (TypeError, {123})]
)
def test_parse_dirs_error(expected_exception, file_path):
    with pytest.raises(expected_exception):
        FileHandler(file_path).parse_dirs()


@pytest.mark.parametrize(
    "file_path, expected_result",
    [
        (
            "tests/test_data/",
            "test_data.txt",
        ),
        (
            "tests/test_data/test.txt",
            "test.txt",
        ),
    ],
)
def test_check_data(file_path, expected_result):
    assert FileHandler(file_path).check_path() == expected_result


@pytest.mark.parametrize(
    "file_path, expected_exception",
    [
        (123, FileNotFoundError),
        (
            "tests/test_data/tt.txt",
            FileNotFoundError,
        ),
    ],
)
def test_check_data_error(file_path, expected_exception):
    with pytest.raises(expected_exception):
        FileHandler(file_path).check_path()


@pytest.fixture(scope="session")
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("sqlite:///hash_sum.db", echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="session")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()


@pytest.fixture(scope="session")
def dataset(db_session):
    file_path_1 = HashSum(file_path="test_data/res/1")
    file_path_2 = HashSum(file_path="test_data/res/2")
    db_session.add(file_path_1)
    db_session.add(file_path_2)
    db_session.commit()
    yield db_session


# def test_database(dataset):
#     session = dataset
#     assert len(session.query(HashSum).all()) == 2
# query = session.query(HashSum).filter(HashSum.file_path == "tests/results/1")
# assert query.first().file_path == "tests/results/1"
