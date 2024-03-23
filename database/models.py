from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(length=40), nullable=True)

    def __str__(self):
        return f'{self.user_id}, {self.name}'

    __repr__ = __str__


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_eng = Column(String(length=40), nullable=False)
    word_rus = Column(String(length=40), nullable=False)

    def __str__(self):
        return f'{self.word_eng}: {self.word_rus}'

    __repr__ = __str__


class UserAddWord(Base):
    __tablename__ = 'user_word'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_eng = Column(String(length=40), nullable=False)
    word_rus = Column(String(length=40), nullable=False)
    user_id = Column(Integer, ForeignKey('user_info.user_id'), nullable=False)


    def __str__(self):
        return f'{self.word_eng}: {self.word_rus}'

    __repr__ = __str__
