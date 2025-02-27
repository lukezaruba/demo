import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello/<name>", methods=["GET"])
def hello(name):
    return jsonify({"message": f"Hello, {name}!"})


@app.route("/goodbye", methods=["GET"])
def goodbye():
    name = request.args.get("name", "?")
    return jsonify({"message": f"Goodbye, {name}!"})


@app.route("/secret", methods=["GET"])
def secret():
    return jsonify({"message": os.environ.get("SECRET")})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
