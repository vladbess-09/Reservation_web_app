import datetime
from sqlalchemy import select, create_engine, ForeignKey, text, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship, joinedload
from config import setting




engine = create_engine(setting.data_base_config, echo=True)
session_maked = sessionmaker(engine)



class Base (DeclarativeBase):

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col} = {getattr(self, col)}")
        return f"object from table: {self.__class__.__name__} {','.join(cols)}"


def create_DB(drop_before_creeate:bool = True):
    if drop_before_creeate:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    else:
        Base.metadata.create_all(engine)

class TableORM(Base):
    __tablename__ = "table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    seats : Mapped[int]
    lockation: Mapped[str]
    reservation: Mapped["ReservationORM"] = relationship(back_populates='table')

    @staticmethod
    def get_all_tables():

        ''' получения всех столов из бд'''

        with session_maked() as sess:
            query = select(TableORM)
            result = sess.execute(query)
            tables = result.scalars().all()
            return tables


    @staticmethod
    def get_table(table_id: int):

        """ получение одного стала из бд """

        with session_maked() as sess:
            query = sess.get(TableORM, table_id)
            return query

    @staticmethod
    def add_new_table(name: str, seats: int, lockation: str):

        """добавление стола"""

        new_table = TableORM(name=name, seats=seats, lockation=lockation)
        with session_maked() as sess:
            sess.add(new_table)
            sess.commit()

    @staticmethod
    def delitte_table(id: int):

        """Удаление стола"""

        with session_maked() as sess:
            sess.execute(delete(TableORM).where(TableORM.id == id))
            sess.commit()


class ReservationORM(Base):
    __tablename__ = "Reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str]
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id", ondelete="CASCADE"))
    time_of_reservation: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    table: Mapped["TableORM"] = relationship(back_populates="reservation")


    @staticmethod
    def get_reservation(id:int):

        """получение конкретной брони из бд"""

        with session_maked() as sess:
            reservation = sess.get(ReservationORM, id)
            return reservation

    @staticmethod
    def get_all_reservation():

        """получение всех броней из бд"""

        with session_maked() as sess:
            query = select(ReservationORM)
            res = sess.execute(query)
            return res.scalars().all()

    @staticmethod
    def add_new_reservation(customer_name: str, table_id: int):

        """добавление новой брони"""

        new_res = ReservationORM(customer_name=customer_name, table_id=table_id)
        with session_maked() as sess:
            sess.add(new_res)
            sess.commit()

    @staticmethod
    def delete_reservation(id: int):

        """удыление брони"""

        with session_maked() as sess:
            sess.delete(sess.get(ReservationORM, id))
            sess.commit()

    @staticmethod
    def select_reservation_with_table(id: int):

        """получение конкретной брони и столика привязанного к ней из бд"""

        with session_maked() as sess:
            query = select(ReservationORM).filter_by(id=id).options(joinedload(ReservationORM.table))
            res = sess.execute(query)
            return res.scalars().all()



