from datetime import datetime, date
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Text, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError


engine = create_engine("sqlite:///booking.db", echo=True)


class Base(DeclarativeBase):
    pass

# гость
class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    contact = Column(String(255), nullable=False, unique=True)

# Отель или владелец апартаментов
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

# Номер / квартира
class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    title = Column(String(150), nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Integer, nullable=False)

    property = relationship("Property", backref="units")

# Бронирование
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)

    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    status = Column(String(50), default="pending") 
    created_at = Column(DateTime, default=datetime.utcnow)

    guest = relationship("Guest", backref="bookings")
    unit = relationship("Unit", backref="bookings")


SessionLocal = sessionmaker(bind=engine)


# функции

def add_guest(name, surname, contact): # добавление гостя
    with SessionLocal() as session:
        try:
            guest = Guest(name=name, surname=surname, contact=contact)
            session.add(guest)
            session.commit()
            print(f"Гость {name} добавлен.")
        except IntegrityError:
            session.rollback()
            print("Ошибка: такой контакт уже существует.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")

def add_property(name, address, description=""): # добавление апартоментов
    with SessionLocal() as session:
        try:
            prop = Property(name=name, address=address, description=description)
            session.add(prop)
            session.commit()
            print(f"Объект '{name}' добавлен.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")

def add_unit(property_id, title, capacity, price_per_night): # добавление квартиры/апартоментов
    with SessionLocal() as session:
        try:
            unit = Unit(
                property_id=property_id,
                title=title,
                capacity=capacity,
                price_per_night=price_per_night
            )
            session.add(unit)
            session.commit()
            print(f"Юнит '{title}' добавлен.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")

def add_booking(guest_id, unit_id, check_in, check_out): # добавления бронирования 
    with SessionLocal() as session:
        try:
            booking = Booking(
                guest_id=guest_id,
                unit_id=unit_id,
                check_in=check_in,
                check_out=check_out,
                status="confirmed"
            )
            session.add(booking)
            session.commit()
            print("Бронирование создано.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при бронировании: {e}")

# создание БД
if __name__ == "__main__":
    Base.metadata.create_all(engine)
 
