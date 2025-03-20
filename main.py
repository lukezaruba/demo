import os

import psycopg2
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder=".")


CONNECTION = {
    "database": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}


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


@app.route("/data", methods=["GET"])
def data():
    return jsonify({"datasets": ["accidents", "cities", "roads"]})


@app.route("/data/accidents", methods=["GET"])
def accidents():
    output = fetch_data("dbo.accidents")
    return jsonify(output)


@app.route("/data/cities", methods=["GET"])
def cities():
    output = fetch_data("dbo.cities")
    return jsonify(output)


@app.route("/data/roads", methods=["GET"])
def roads():
    output = fetch_data("dbo.roads")
    return jsonify(output)


def fetch_data(table_name):
    with psycopg2.connect(**CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                    SELECT JSON_BUILD_OBJECT('type', 'FeatureCollection',
                    'features', JSON_AGG(ST_AsGeoJSON({table_name}.*)::json)) FROM {table_name};
            """)

            return cur.fetchone()[0]


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
