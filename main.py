from flask import Flask, render_template, request

app = Flask(__name__)

#this is the login page
@app.route("/")
def login_page():
	return render_template("login.html")

@app.route("/scholarmain")
def scholarmain():
	return render_template("scholarmain.html")

@app.route("/staffmain")
def staffmain():
	return render_template("staffmain.html")

if __name__ == "__main__":
	app.run(debug=True)