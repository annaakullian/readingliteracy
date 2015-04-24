from flask import Flask, render_template, request, session, redirect, flash, url_for, make_response
from model import Scholar, Goal, Book, BookLog, session as dbsession
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
    goal_number = request.form['goal_number']
    goal_description = request.form['goal_description']
    strength_or_endurance = "strength"
    user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
    goal = Goal(goal_number=goal_number, goal_description=goal_description, strength_or_endurance=strength_or_endurance, scholar_id=user_object.id, achieved=False, status=0)
    dbsession.add(goal)
    dbsession.commit()
    return redirect("/activegoals")

@app.route("/addendurancegoal", methods=['GET'])
def addendurancegoal():
    return render_template("addendurancegoal.html", user=session['user'])

@app.route("/addendurancegoal", methods=['POST'])
def digestendurancegoal():
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
    """
    School Library displays all books that the scholar
    has read as well as their book covers and
    ratings.

    """
    user = session['user']
    scholar_id = dbsession.query(Scholar).filter_by(name=user).first().id
    booklogs = dbsession.query(BookLog).filter_by(scholar_id=scholar_id).all()
    book_dictionary = {}
    if booklogs:
        for book_log in booklogs:
            book = dbsession.query(Book).filter_by(id=book_log.book_id).first()
            book_dictionary[book] = book_log.rating

    return render_template("scholarlibrary.html", user=user, book_dictionary=book_dictionary)


@app.route("/addbook", methods=["GET"])
def addbook():
    return render_template("addbook.html", user=session['user'])


@app.route("/addbook", methods=["POST"])
def digestaddbook():
    """
    Add a book to the database.
    """
    book_title = request.form['title']
    book_author = request.form['author']
    book_rating = request.form['rating']
    user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
    book = dbsession.query(Book).filter_by(title=book_title).filter_by(author=book_author).first()
    if not book:
        title_for_url = book_title.replace(" ", "%20")
        file = urllib2.urlopen('http://www.librarything.com/api/thingTitle/%s' % (title_for_url))
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        idlist_dictionary = data.get(u'idlist', None)
        isbn_number = idlist_dictionary.get([u'isbn'][0], None)
        if isbn_number is None:
            cover_url = "http://www.readingforpleasure.net/wp-content/uploads/2012/01/cat-reading-book.jpg"
        else:
            while isinstance(isbn_number, list):
                    isbn_number = isbn_number[0]
            cover_url = "http://covers.openlibrary.org/b/isbn/%s-L.jpg" % (isbn_number)
        book_to_add = Book(author=book_author, title=book_title, isbn=isbn_number, cover_url=cover_url)
        dbsession.add(book_to_add)
        dbsession.commit()
        book = dbsession.query(Book).filter_by(title=book_title).filter_by(author=book_author).first()
    book_log = BookLog(book_id=book.id, scholar_id=user_object.id, rating=book_rating)
    dbsession.add(book_log)
    dbsession.commit()
    return redirect("/scholarlibrary")


if __name__ == "__main__":
    app.run(debug=True)
