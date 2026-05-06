from datetime import datetime
from sqlalchemy import create_engine , Column , Integer , DateTime , Text , String
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Session
from sqlalchemy.exc import IntegrityError

engine = create_engine("sqlite:///BD.db", echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column (String(100), nullable=False)
    fatherland = Column (String(100), nullable=False)
    contact = Column(String(255), nullable=False, unique=True)

class Master(Base):
    __tablename__ = 'masters'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column (String(100), nullable=False)
    fatherland = Column (String(100), nullable=False)
    bio = Column (Text, nullable=False)

class Freedom_time(Base):
    __tablename__ = 'freedom_time'
    
    id = Column (Integer, primary_key=True)
    time = Column (DateTime, default=datetime.utcnow)
    master = Column (Integer)
    condition = Column (Integer)    
    
    
    
SessionLocal = sessionmaker(bind=engine)


def add_user(name, surname, fatherland, contact):
    with SessionLocal() as session:
        try:
            new_user = User(name=name, surname=surname, fatherland=fatherland, contact=contact)
            session.add(new_user)
            session.commit()
            print(f"Пользователь {name} добавлен.")
        except IntegrityError:
            session.rollback()
            print(f"Ошибка: Пользователь с контактом {contact} уже существует.")
        except Exception as e:
            session.rollback()
            print(f"Произошла ошибка: {e}")

def add_freedom_time(master_id, condition_val, specific_time=None):
    with SessionLocal() as session:
        try:
            new_time = Freedom_time(
                master=master_id, 
                condition=condition_val,
                time=specific_time if specific_time else datetime.now()
            )
            session.add(new_time)
            session.commit()
            print("Запись о времени добавлена.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении времени: {e}")

def add_master(name, surname, fatherland, bio):
    with SessionLocal() as session:
        try:
            new_master = Master(name=name, surname=surname, fatherland=fatherland, bio=bio)
            session.add(new_master)
            session.commit()
            print(f"Мастер {name} добавлен.")
        except Exception as e:
            session.rollback()
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    
    add_master("Александр", "Пушкин", "Сергеевич", "Мастер по бакенбардам и классическим стрижкам.")
    add_master("Виктор", "Цой", "Робертович", "Стригу под 'восьмиклассницу'. Перемены требуют наших глаз.")
    add_master("Джон", "Уик", "—", "Стригу быстро, чисто, профессионально. Карандаш не использую.")
    add_freedom_time(master_id, 1, datetime(2026, 4, 25, 10, 0))
    add_freedom_time(master_id, 2, datetime(2026, 4, 25, 14, 0))
    add_freedom_time(master_id, 3, datetime(2026, 4, 26, 12, 0))


 
