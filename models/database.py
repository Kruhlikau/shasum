# Standard library imports
from typing import Any, List, Tuple

# Related third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, String, Integer

# Local imports
from file_hash import FileHandler, console_logger
from config import __tablename__

Base: Any = declarative_base()
engine = create_engine("sqlite:///hash_sum.db", echo=False)
session = sessionmaker(bind=engine)()


class HashSum(Base):
    __tablename__ = __tablename__
    id = Column(Integer, primary_key=True)
    file_path = Column(String)

    def __repr__(self):
        return self.file_path


Base.metadata.create_all(engine)


class DataInteraction:
    saved = False
    results: List[Tuple[str, str]] = []

    def __init__(self, data: List[Tuple[str, str]], file_path: str):
        """
        :param data: list of tuples[hash_sum, file_path]
        :param file_path: directory path
        """
        self.data = data
        self.file_path = file_path
        self.path: str = FileHandler(self.file_path).check_path()

    def check_data(self):
        """
        check result with output[hash_sum file_path OK/NOT OK]
        :return: list of tuples[hash_sum, file_path]
        """
        query = session.query(HashSum).filter(HashSum.file_path == self.path)
        try:
            with open(f"results/{query.first()}") as f:
                for num, line in enumerate(f):
                    res = "FAILED"
                    if line.split()[0] == self.data[num][0]:
                        res = "OK"
                    console_logger.info(f"{line[:-1]} {res}")
                    self.results.append((line[:-1], res))
            return self.results
        except FileNotFoundError:
            console_logger.error("No such file or directory to check in db")

    def save_data(self) -> bool:
        """
        :return: None
        """
        with open(f"results/{self.path}", "w") as f:
            for hash_sum, file in self.data:
                f.write(f"{hash_sum} {file}\n")
        res = HashSum(file_path=f"{self.path}")
        last_count = session.query(HashSum).count()
        session.add(res)
        session.commit()
        new_count = session.query(HashSum).count()
        if last_count + len(self.data) == new_count:
            self.saved = True
        return self.saved
