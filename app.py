from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"
VALID_NAMES = ["Виктор", "Эми", "Леша"]  # Pre-defined list of names

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all valid names have an entry, defaulting to 0
            for name in VALID_NAMES:
                if name not in data:
                    data[name] = 0.0
            return data
    # Initialize with all valid names at 0 km
    return {name: 0.0 for name in VALID_NAMES}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    if request.method == "POST":
        name = request.form["name"]
        if name in VALID_NAMES:  # Only process if name is valid
            km = float(request.form["km"])
            data[name] = data.get(name, 0.0) + km
            save_data(data)
        return redirect("/")

    # Sort by kilometers and find max for percentage with fallback
    sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
    max_km = max(sorted_data.values()) if sorted_data.values() else 1  # Fallback to 1 if all values are 0
    return render_template("index.html", data=sorted_data, max_km=max_km, valid_names=VALID_NAMES)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)