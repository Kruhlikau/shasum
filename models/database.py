# Standard library imports
from typing import Any

# Related third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, String, Integer, and_

Base: Any = declarative_base()
engine = create_engine("sqlite:///hash_sum.db", echo=False)
session = sessionmaker(bind=engine)()


class HashSum(Base):
    __tablename__ = "hash_sum"
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    hash_sum = Column(String)

    def __repr__(self):
        return self.file_path


Base.metadata.create_all(engine)


def safe_data(table, file_path: str, hash_sum: str) -> None:
    """

    :param table: db for data
    :param file_path: directory path
    :param hash_sum: hash sum of the file
    :return: None
    """
    res = table(file_path=file_path, hash_sum=hash_sum)
    session.add(res)
    session.commit()


def check_data(table, file_path: str, hash_sum: str) -> bool:
    """

    :param table: db for data check
    :param file_path: directory path
    :param hash_sum: hash sum of the file
    :return: check result[bool]
    """
    query = session.query(table).filter(
        and_(table.file_path == file_path, table.hash_sum != hash_sum)
    )
    return False if query.first() else True
