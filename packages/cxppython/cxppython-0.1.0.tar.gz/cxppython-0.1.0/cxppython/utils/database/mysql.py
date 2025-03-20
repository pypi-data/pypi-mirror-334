from typing import Iterable,List, Type

from sqlalchemy import text,insert,create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import as_declarative
import cxppython as cc

@as_declarative()
class Base:
    pass

class MysqlDB:
    __instance = None

    def __init__(self, mysql_config):
        if MysqlDB.__instance is not None:
            raise Exception("This class is a singleton, use DB.create()")
        else:
            MysqlDB.__instance = self
        self.engine = self.create_engine(mysql_config)
        self.session = sessionmaker(bind=self.engine)

    @staticmethod
    def instance():
        return MysqlDB.__instance

    @staticmethod
    def session() -> Session:
        session = MysqlDB.__instance.session
        return session()

    @staticmethod
    def add(value) -> Exception | None:
        try:
            session = MysqlDB.session()
            session.add(value)
            session.commit()
            session.close()
        except Exception as err:
            return err

        return None

    @staticmethod
    def bulk_save(objects: Iterable[object]) -> Exception | None:
        try:
            with MysqlDB.session() as session, session.begin():
                session.bulk_save_objects(objects)
        except Exception as err:
            return err

        return None

    @staticmethod
    def create(mysql_config):
        if MysqlDB.__instance is None:
            MysqlDB.__instance = MysqlDB(mysql_config)

    @staticmethod
    def test_db_connection():
        try:
            # 尝试建立连接
            with MysqlDB.instance().engine.connect() as connection:
                cc.logging.success("Database connection successful!")
                connection.commit()
                return True
        except OperationalError as e:
            cc.logging.error(f"Failed to connect to the database: {e}")
            return False

    def create_engine(self, mysql_config):
        echo = False
        if "echo" in mysql_config:
            echo = mysql_config["echo"]
        return create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**mysql_config),
            pool_size=200,
            max_overflow=0,
            echo=echo)

    def connect(self):
        return self.engine.connect()

    def batch_insert_records(session: Session,
                             model: Type[Base],
                             records: List,
                             batch_size: int = 50,
                             ignore_existing: bool = True,
                             commit_per_batch: bool = True):
        data = records
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            stmt = insert(model).values(batch)
            if ignore_existing:
                stmt = stmt.prefix_with("IGNORE")

            try:
                session.execute(stmt)
            except Exception as e:
                cc.logging.error(f"Batch insert failed at index {i}: {e}")
                session.rollback()
                raise

            if commit_per_batch:
                session.commit()

