from flask import Flask, render_template, request, session, redirect, flash, url_for, make_response
from model import Scholar, Goal, Book, BookLog, Rating, session as dbsession
import os
import json
from lxml import html, etree
import requests
from io import StringIO, BytesIO
import urllib2
import xmltodict
from collections import OrderedDict


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect("/")


@app.route("/addscholar")
def addscholar():
    return render_template("addscholar.html")


@app.route("/addnewscholar", methods=['GET', 'POST'])
def addnewscholar():
    scholar_name = request.form['scholar_name']
    scholar_school = request.form['scholar_school']
    scholar_grade = request.form['grade']
    user = dbsession.query(Scholar).filter_by(name=scholar_name).first()
    if user:
        error = "You already have an account. Please login Here"
        return render_template("login.html", error=error)
    else:
        user = Scholar(name=scholar_name, school=scholar_school, grade=scholar_grade)
        dbsession.add(user)
        dbsession.commit()
        return redirect("/")


@app.route("/scholarmain", methods=['GET', 'POST'])
def scholarmain():
    scholar_name = request.form['scholar_name']
    user = dbsession.query(Scholar).filter_by(name=scholar_name).first()
    if not user:
        error = "Make sure your name is spelled correctly!"
        return render_template("login.html", error=error)
    else:
        #check to make sure user is in the database. if not, say to check spelling and try again"
        #put user into session
        session['user'] = user.name
        scholar_id = dbsession.query(Scholar).filter_by(name=user.name).first().id
        goals = dbsession.query(Goal).filter_by(scholar_id=scholar_id).all()

        if len(goals)>=2:
            return render_template("scholarmain2.html", scholar_name=user.name, scholar_school=user.school)
        else:
            return render_template("scholarmain.html", scholar_name=user.name, scholar_school=user.school)


@app.route("/staffmain")
def staffmain():
    return render_template("staffmain.html")

@app.route("/activegoals")
def activegoals():
    user = session['user']
    scholar_id = dbsession.query(Scholar).filter_by(name=user).first().id
    # scholar_id = scholar.id
    goals = dbsession.query(Goal).filter_by(scholar_id=scholar_id).all()
    return render_template("activegoals.html", user=session['user'], goals=goals)


@app.route('/editstrengthgoal/<int:goalid>')
def editgoal(goalid):
    goal = dbsession.query(Goal).filter_by(id=goalid).first()
    return render_template("editgoal.html", goal=goal)

@app.route('/editstrengthgoal/<int:goalid>', methods=['POST'])
def digesteditgoal(goalid):
    goal = dbsession.query(Goal).filter_by(id=goalid).first()
    goal_number = request.form['goal_number']
    goal_description = request.form['goal_description']
    goal.goal_number = goal_number
    goal.goal_description = goal_description
    dbsession.commit()
    return redirect("/activegoals")

@app.route('/editendurancegoal/<int:goalid>')
def editendurancegoal(goalid):
    goal = dbsession.query(Goal).filter_by(id=goalid).first()
    return render_template("editendurancegoal.html", goal=goal)

@app.route('/editendurancegoal/<int:goalid>', methods=['POST'])
def digesteditendurancegoal(goalid):
    goal = dbsession.query(Goal).filter_by(id=goalid).first()
    goal_number = request.form['goal_number']
    goal_description = request.form['goal_description']
    goal.goal_number = goal_number
    goal.goal_description = goal_description
    dbsession.commit()
    return redirect("/activegoals")

@app.route("/addgoal", methods=['GET'])
def addgoal():
    return render_template("addgoal.html", user=session['user'])

@app.route("/addgoal", methods=['POST'])
def digestgoal():
    #add goal into the database
    goal_number = request.form['goal_number']
    goal_description = request.form['goal_description']
    strength_or_endurance = "strength"
    user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
    goal = Goal(goal_number=goal_number, goal_description=goal_description, strength_or_endurance=strength_or_endurance, scholar_id=user_object.id, achieved=False, status=0)
    dbsession.add(goal)
    dbsession.commit()
    return redirect("/activegoals")
    #add to database
    #show in active goals

@app.route("/addendurancegoal", methods=['GET'])
def addendurancegoal():
    return render_template("addendurancegoal.html", user=session['user'])

@app.route("/addendurancegoal", methods=['POST'])
def digestendurancegoal():
    #add goal into the database
    goal_number = request.form['goal_number']
    goal_description = request.form['goal_description']
    strength_or_endurance = "endurance"
    user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
    goal = Goal(goal_number=goal_number, goal_description=goal_description, strength_or_endurance=strength_or_endurance, scholar_id=user_object.id, achieved=False, status=0)
    dbsession.add(goal)
    dbsession.commit()
    return redirect("/activegoals")


@app.route("/goalgallery")
def goalgallery():
    user = session['user']
    scholar_id = dbsession.query(Scholar).filter_by(name=user).first().id
    goals = dbsession.query(Goal).filter_by(scholar_id=scholar_id).all()
    return render_template("goalgallery.html", user=session['user'], goals=goals)


@app.route("/scholarlibrary")
def scholarlibrary():
    user = session['user']
    print "got here"
    scholar_id = dbsession.query(Scholar).filter_by(name=user).first().id
    booklogs = dbsession.query(BookLog).filter_by(scholar_id=scholar_id).all()
    #book list is a list of book objects read by user
    book_list = []
    rating_dictionary = {}
    xml_dictionary = {}
    if booklogs:
        bookids = [i.book_id for i in booklogs]
        for book_id in bookids:
            book = dbsession.query(Book).filter_by(id=book_id).first()
            book_list.append(book)
    print "book list", book_list
    for book in book_list:
        print "mom book list", book_list
        file = urllib2.urlopen('http://www.librarything.com/api/thingTitle/%s' % (book.title))
        print "my file", file
        data = file.read()
        file.close()
        print "flower", data
        data = xmltodict.parse(data)
        print "my data", data
        xml_dictionary[book] = data
        print "myy dictionary", xml_dictionary

        book_id = book.id
        rating = dbsession.query(Rating).filter_by(book_id=book_id).first()
        if rating:
            rating_dictionary[book] = [rating]
        else:
            rating_dictionary[book] = ["rate this book"]
    isbn_dictionary = {}
    for book in xml_dictionary.keys():
        book_id = book.id
        book_object = dbsession.query(Book).filter_by(id=book_id).first()
        isbn_number_from_db = book_object.isbn
        if not isbn_number_from_db:
            diction = xml_dictionary[book]
            isbn_number = diction.get(u'idlist', None)
            isbn_number2 = isbn_number.get([u'isbn'][0], None)
            while isinstance(isbn_number2, list):
                isbn_number2 = isbn_number2[0]
            # int_isbn_number = int(str((isbn_number2)))
            if len(str(isbn_number2))==9:
                isbn_number2 = "0" + str(isbn_number2)
            elif len(str(isbn_number2))==9:
                isbn_number2 = "00" + str(isbn_number2)
            else:
                isbn_number2 = isbn_number2
            book_object.isbn = isbn_number2
            dbsession.commit()
    for book in rating_dictionary.keys():
        book_isbn = book.isbn
        length_isbn = len(str(book_isbn))
        if length_isbn==9:
            book_isbn = "0" + str(book_isbn)
        elif length_isbn==8:
            book_isbn = "00" + str(book_isbn)
        else:
            book_isbn = book.isbn
        value_to_append = [book_isbn]
        old_value = rating_dictionary.get(book, [])
        new_value = old_value + value_to_append
        rating_dictionary[book] = new_value
        print rating_dictionary[book]
        print rating_dictionary[book][0].rating

    return render_template("scholarlibrary.html", user=user, isbn_dictionary=isbn_dictionary, rating_dictionary=rating_dictionary)


@app.route("/addbook", methods=["GET"])
def addbook():
    return render_template("addbook.html", user=session['user'])


@app.route("/addbook", methods=["POST"])
def digestaddbook():
    #add goal into the database
    book_title = request.form['title']
    book_author = request.form['author']
    book_rating = request.form['rating']
    user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
    book = dbsession.query(Book).filter_by(title=book_title).filter_by(author=book_author).first()
    if not book:
        book_to_add = Book(author=book_author, title=book_title)
        dbsession.add(book_to_add)
        dbsession.commit()
        book = dbsession.query(Book).filter_by(title=book_title).filter_by(author=book_author).first()
    book_log = BookLog(book_id = book.id, scholar_id=user_object.id)
    dbsession.add(book_log)
    rating = Rating(book_id=book.id, scholar_id=user_object.id, rating=book_rating)
    dbsession.add(rating)
    dbsession.commit()
    return redirect("/scholarlibrary")

if __name__ == "__main__":
    app.run(debug=True)