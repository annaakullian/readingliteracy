from flask import Flask, render_template, request

app = Flask(__name__)

#this is the login page
@app.route("/")
def login_page():
	return render_template("login.html")

if __name__ == "__main__":
	app.run(debug=True)