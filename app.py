from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello World"

@app.route("/home")
def home():
    return "This is home page"

from controller import *

if __name__ == "__main__":
    app.run(debug=True)