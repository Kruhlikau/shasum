# Standard library imports
from typing import Any

# Related third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, String, Integer

# Local imports
from file_hash import check_path, console_logger

Base: Any = declarative_base()
engine = create_engine("sqlite:///hash_sum.db", echo=False)
session = sessionmaker(bind=engine)()


class HashSum(Base):
    __tablename__ = "hash_sum"
    id = Column(Integer, primary_key=True)
    file_path = Column(String)

    def __repr__(self):
        return self.file_path


Base.metadata.create_all(engine)


def check_data(file_path: str, result: list) -> None:
    """
    check result with output[hash_sum file_path OK/NOT OK]
    :param file_path: directory path
    :param result: list of tuples[hash_sum, file_path]
    :return: None
    """
    path = check_path(file_path)
    query = session.query(HashSum).filter(HashSum.file_path == path)
    try:
        with open(f"results/{query.first()}") as f:
            for num, line in enumerate(f):
                condition = line.split()[0] == result[num][0]
                res = "OK" if condition else "NOT OK"
                console_logger.info(f"{line[:-1]} {res}")
    except FileNotFoundError:
        console_logger.error("No such file or directory to check in db")


def save_data(data: list, file_path: str) -> None:
    """
    :param data: list of tuples[hash_sum, file_path]
    :param file_path: directory path
    :return: None
    """
    path = check_path(file_path)
    with open(f"results/{path}", "w") as f:
        for hash_sum, file in data:
            f.write(f"{hash_sum} {file}\n")
    res = HashSum(file_path=f"{path}")
    session.add(res)
    session.commit()
