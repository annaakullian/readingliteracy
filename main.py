from flask import Flask, render_template, request, session, redirect, flash
from model import Scholar, Goal, Book, BookLog, Rating, session as dbsession
import os
import json

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#this is the login page
@app.route("/")
def login_page():
	return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	session.pop('username', None)
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
		session['user'] = user.name
		return render_template("scholarmain.html", scholar_name=user.name, scholar_school=user.school)

@app.route("/staffmain")
def staffmain():
	return render_template("staffmain.html")

@app.route("/activegoals")
def activegoals():
	return render_template("activegoals.html", user=session['user'])

@app.route("/addgoal", methods=['GET'])
def addgoal():
	return render_template("addgoal.html", user=session['user'])

@app.route("/addgoal", methods=['POST'])
def digestgoal():
	#add goal into the database 
	goal_number = request.form['goal_number']
	goal_description = request.form['goal_description']
	user_object = dbsession.query(Scholar).filter_by(name=session['user']).first()
	goal = Goal(goal_number=goal_number, goal_description=goal_description, scholar_id=user_object.id, achieved=False, status=0) 
	dbsession.add(goal)
	dbsession.commit()
	return redirect("/activegoals")
	#add to database
	#show in active goals 

@app.route("/goalgallery")
def goalgallery():
	return render_template("goalgallery.html")

@app.route("/scholarlibrary")
def scholarlibrary():
	return render_template("scholarlibrary.html")



if __name__ == "__main__":
	app.run(debug=True)