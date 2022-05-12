# # Local imports
# from models.database import Base
#
# # Related third party imports
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
#
# @pytest.fixture(scope="session")
# def connection():
#     engine = create_engine("sqlite:///hash_sum.db", echo=False)
#     return engine.connect()
#
#
# @pytest.fixture(scope="session")
# def setup_database(connection):
#     Base.metadata.bind = connection
#     Base.metadata.create_all()
#
#     yield
#
#     Base.metadata.drop_all()
#
#
# @pytest.fixture(scope="session")
# def db_session(setup_database, connection):
#     transaction = connection.begin()
#     yield scoped_session(
#         sessionmaker(autocommit=False, autoflush=False, bind=connection)
#     )
#     transaction.rollback()
