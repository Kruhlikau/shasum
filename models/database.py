# Standard library imports
from typing import Any, List, Tuple

# Related third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, String, Integer

# Local imports
from file_hash import FileHandler, console_logger

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


class DataInteraction:
    def __init__(self, data: List[Tuple[str, str]], file_path: str):
        """
        :param data: list of tuples[hash_sum, file_path]
        :param file_path: directory path
        """
        self.data = data
        self.file_path = file_path

    def check_data(self) -> None:
        """
        check result with output[hash_sum file_path OK/NOT OK]
        :return: None
        """
        path = FileHandler(self.file_path).check_path()
        query = session.query(HashSum).filter(HashSum.file_path == path)
        try:
            with open(f"results/{query.first()}") as f:
                for num, line in enumerate(f):
                    res = "FAILED"
                    if line.split()[0] == self.data[num][0]:
                        res = "OK"
                    console_logger.info(f"{line[:-1]} {res}")
        except FileNotFoundError:
            console_logger.error("No such file or directory to check in db")

    def save_data(self) -> None:
        """
        :return: None
        """
        path = FileHandler(self.file_path).check_path()
        with open(f"results/{path}", "w") as f:
            for hash_sum, file in self.data:
                f.write(f"{hash_sum} {file}\n")
        res = HashSum(file_path=f"{path}")
        session.add(res)
        session.commit()
