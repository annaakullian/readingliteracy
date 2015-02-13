"""Database models for readingviz. 
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os

#change the url to env variable

#Association proxy (bit over-detailed) http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/associationproxy.html
#http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html look for One to One section

#engine is connecion to db
engine = create_engine("postgres://localhost:5432/readingviz", echo=True)

#connection negotiation-talks to db 
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()


#inherit from a time stamp class
#database index: 
#association proxy: 

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
	scholar_id = Column(Integer, ForeignKey('scholars.id'))
	achieved = Column(Boolean, nullable = True)
	status = Column(Integer, nullable = True)

	scholar = relationship("Scholar", backref=backref("scholars", order_by=id))
	#look to see if foreing key to cscholar class

#this table keeps track of all books
class Book(Base):
	__tablename__="books"
	id = Column(Integer, primary_key = True)
	author = Column(String(500), nullable = True)
	title = Column(String(1000), nullable = True)

#this table stores which books scholars have read
class BookLog(Base):
	__tablename__="booklogs"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey('books.id'))
	scholar_id = Column(Integer, ForeignKey('books.id'))

	book = relationship("Book", backref=backref("books", order_by=id))
	scholar = relationship("Scholar", backref=backref("scholars", order_by=id))

#this table stores ratings for each book-scholar pair
class Rating(Base):
	__tablename__="ratings"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey('books.id'))
	scholar_id = Column(Integer, ForeignKey('books.id'))
	rating = Column(Integer, primary_key = True)

	book = relationship("Book", backref=backref("books", order_by=id))
	scholar = relationship("Scholar", backref=backref("scholars", order_by=id))


if __name__ == "__main__":
	Base.metadata.create_all(engine)
