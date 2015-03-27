"""Database models for readingviz. 
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger 
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
# from datetime import datetime 
import os


#engine is connecion to db
engine = create_engine(os.environ.get("DATABASE_URL"), echo=True)

#connection negotiation-talks to db 
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

#association proxy: 
#all tables inherit from timestamp and base
# class AutoTimestamp(object):
#     created_at = Column(DateTime, default=datetime.utcnow,
#                         nullable=True)
#     updated_at = Column(DateTime, default=datetime.utcnow,
#                         onupdate=datetime.utcnow, nullable=True)

#these are the scholars
class Scholar(Base):
	__tablename__= "scholars"

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = True)
	school = Column(String(100), nullable = True)
	grade = Column(String(100), nullable = True)
	last_log_in = Column(DateTime, nullable = True)
	#scholars = relationship goal

#keeps track of all of the scholar's goals. Many to one relationshipt with Scholars
class Goal(Base):
	__tablename__="goals"

	id = Column(Integer, primary_key = True)
	goal_number = Column(Integer, nullable = True)
	goal_description = Column(String(1000), nullable = True)
	strength_or_endurance = Column(String(1000), nullable = True)
	scholar_id = Column(Integer, ForeignKey('scholars.id'))
	achieved = Column(Boolean, nullable = True)
	status = Column(Integer, nullable = True)

	scholar = relationship("Scholar", backref=backref("goals", order_by=id))
	#look to see if foreing key to cscholar class

class TimeGoals(Base):
	__tablename__="timegoals"

	id = Column(Integer, primary_key = True)
	timegoal_number = Column(Integer, nullable = True)
	scholar_id = Column(Integer, ForeignKey('scholars.id'))
	achieved = Column(Boolean, nullable = True)

	scholar = relationship("Scholar", backref=backref("timegoals", order_by=id))

#this table keeps track of all books
class Book(Base):
	__tablename__="books"
	id = Column(Integer, primary_key = True)
	author = Column(String(500), nullable = True)
	title = Column(String(1000), nullable = True)
	isbn = Column(BigInteger, nullable=True)

#this table stores which books scholars have read
class BookLog(Base):
	__tablename__="booklogs"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey('books.id'))
	scholar_id = Column(Integer, ForeignKey('scholars.id'))

	book = relationship("Book", backref=backref("booklogs", order_by=id))
	scholar = relationship("Scholar", backref=backref("booklogs", order_by=id))

#this table stores ratings for each book-scholar pair
class Rating(Base):
	__tablename__="ratings"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey('books.id'))
	scholar_id = Column(Integer, ForeignKey('scholars.id'))
	rating = Column(Integer, primary_key = True)

	book = relationship("Book", backref=backref("ratings", order_by=id))
	scholar = relationship("Scholar", backref=backref("ratings", order_by=id))


if __name__ == "__main__":
	Base.metadata.create_all(engine)
