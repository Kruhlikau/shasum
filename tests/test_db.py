# Related third party imports
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
import pytest

# Standard library imports
from typing import Any
from datetime import date
import os

# Local imports
from config import __tablename__
from models.database import DataInteraction
from tests.static.utils import test_data

TestBase: Any = declarative_base()


class HashSumTest(TestBase):
    __tablename__ = __tablename__ + f"_test_{date.today()}"
    id = Column(Integer, primary_key=True)
    file_path = Column(String)

    def __repr__(self):
        return self.file_path


class TestDB:
    def db_engine(self):
        """
        returns a SQLAlchemy engine
         which is suppressed after the test session
        """
        self.db_server = "sqlite:///hash_sum_test.db"
        self.engine = create_engine(self.db_server)
        return self.engine

    def db_session(self):
        """returns a SQLAlchemy session"""
        session = sessionmaker(bind=self.db_engine())
        self.session = session()
        return self.session

    def dataset(self):
        """initial dataset for tests"""
        file_path_1 = HashSumTest(file_path="tests_results")
        file_path_2 = HashSumTest(file_path="testdata/res/2")
        self.session.add_all([file_path_1, file_path_2])
        self.session.commit()

    def setup(self):
        """setup test db with test dataset"""
        self.db_session()
        TestBase.metadata.create_all(self.engine)
        self.dataset()

    def setup_test_dataset(self, data, file_path):
        test_dataset = DataInteraction(file_path=file_path, data=data)
        test_dataset.db_session = self.session
        return test_dataset

    def test_dataset(self):
        assert self.session.query(HashSumTest).count() == 2

    def test_dataset_first(self):
        exp_res = "tests_results"
        assert str(self.session.query(HashSumTest).first()) == exp_res

    def test_add_item(self):
        file_path_3 = HashSumTest(file_path="testdata/res/3")
        self.session.add(file_path_3)
        self.session.commit()
        assert str(self.session.query(HashSumTest).get(3)) == "testdata/res/3"

    def test_delete_item(self):
        pre_items_count = int(self.session.query(HashSumTest).count())
        first_item = self.session.query(HashSumTest).first()
        self.session.delete(first_item)
        self.session.commit()
        current_items_count = int(self.session.query(HashSumTest).count())
        assert current_items_count == pre_items_count - 1

    def test_update_item(self):
        first_item = self.session.query(HashSumTest).get(1)
        first_item.file_path = "123"
        self.session.add(first_item)
        self.session.commit()
        assert str(self.session.query(HashSumTest).first().file_path) == "123"

    @pytest.mark.parametrize("data, file_path, expected_result", test_data)
    def test_save_data(self, data, file_path, expected_result):
        test_dataset = self.setup_test_dataset(file_path=file_path, data=data)
        assert test_dataset.save_data(db=HashSumTest) is True
        os.remove(f"results/{test_dataset.path}")

    @pytest.mark.parametrize("data, file_path, expected_result", test_data)
    def test_check_data(self, data, file_path, expected_result):
        test_dataset = self.setup_test_dataset(file_path=file_path, data=data)
        test_dataset.save_data(db=HashSumTest)
        assert test_dataset.check_data(db=HashSumTest) == [expected_result]
        os.remove(f"results/{test_dataset.path}")

    def teardown(self):
        TestBase.metadata.drop_all(bind=self.engine)
        db_file = self.db_server.split("///")[-1]
        os.remove(db_file)
