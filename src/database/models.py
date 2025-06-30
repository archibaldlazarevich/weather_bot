from sqlalchemy import Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    tel_id: Mapped[int] = mapped_column(Integer, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
