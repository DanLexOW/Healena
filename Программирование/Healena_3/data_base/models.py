from sqlalchemy import String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class Training(Base):
    __tablename__ = 'training'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(150))
    sex: Mapped[str] = mapped_column(String(150))
    common_muscle_group: Mapped[str] = mapped_column(String(150))
    detailed_muscle_group: Mapped[str] = mapped_column(String(150))
    weight_loss: Mapped[str] = mapped_column(String(150))
    weight_gain: Mapped[str] = mapped_column(String(150))
    keep_shape: Mapped[str] = mapped_column(String(150))
    energy_feelins: Mapped[str] = mapped_column(String(150))
    solo: Mapped[str] = mapped_column(String(150))



class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    belok: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    fat: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    carbohydrate: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    kkal: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    category: Mapped[str] = mapped_column(String(150))


class Uniduct(Base):
    __tablename__ = 'uniduct'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(150), nullable=False)

class User_data(Base):
    __tablename__ = 'user_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    calc_data: Mapped[str] = mapped_column(String(150), nullable=False)
    send: Mapped[str] = mapped_column(String(150), nullable=False)

