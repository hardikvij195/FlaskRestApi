from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, Hardik!"


@app.route("/api/sum/")
def sum():
    return "Get Sum!"


@app.route("/api/getno/<int:n>")
def getnum(n):
    res = {
        "num": n
    }
    return res


@app.route("/api/name/<name>")
def name(name):
    return name


if __name__ == "__main__":
    app.run(debug=True)
