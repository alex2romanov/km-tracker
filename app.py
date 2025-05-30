# from flask import Flask, render_template, request, redirect
# import json
# import os
#
# app = Flask(__name__)
#
# DATA_FILE = "data.json"
#
# def load_data():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     return {"Виктор": 0, "Эми": 0, "Леша": 0}
#
# def save_data(data):
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     data = load_data()
#     if request.method == "POST":
#         name = request.form["name"]
#         km = float(request.form["km"])
#         data[name] = data.get(name, 0) + km
#         save_data(data)
#         return redirect("/")
#
#     # сортируем по километрам
#     sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
#     return render_template("index.html", data=sorted_data)
#
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"Виктор": 0, "Эми": 0, "Леша": 0}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    if request.method == "POST":
        name = request.form["name"]
        km = float(request.form["km"])
        data[name] = data.get(name, 0) + km
        save_data(data)
        return redirect("/")

    # Sort by kilometers and find max for percentage
    sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
    max_km = max(sorted_data.values()) if sorted_data else 1
    return render_template("index.html", data=sorted_data, max_km=max_km)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

