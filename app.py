from flask import Flask, render_template, request, redirect
import json
import os
import traceback

app = Flask(__name__)
print("Flask app initialized")

# Список допустимых имен
VALID_NAMES = ["Виктор", "Эми", "Леша"]
print(f"VALID_NAMES: {VALID_NAMES}")

# Путь к файлу данных
DATA_FILE = os.environ.get("DATA_FILE", "/data/data.json")
print(f"DATA_FILE set to: {DATA_FILE}")


def ensure_data_file():
    print("Entering ensure_data_file")
    data_dir = os.path.dirname(DATA_FILE)
    try:
        if data_dir and not os.path.exists(data_dir):
            print(f"Creating directory: {data_dir}")
            os.makedirs(data_dir)
            os.chmod(data_dir, 0o777)
            print(f"Created directory: {data_dir}")

        if not os.path.exists(DATA_FILE):
            print(f"Creating initial data file: {DATA_FILE}")
            initial_data = {name: 0.0 for name in VALID_NAMES}
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            os.chmod(DATA_FILE, 0o666)
            print(f"Created initial data file: {DATA_FILE}")
        else:
            print(f"Data file {DATA_FILE} already exists, verifying content")
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for name in VALID_NAMES:
                    if name not in data:
                        data[name] = 0.0
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"Verified and updated data file: {data}")
    except Exception as e:
        print(f"Error initializing data file: {e}")
        traceback.print_exc()


def load_data():
    print("Entering load_data")
    try:
        ensure_data_file()
        print(f"Reading data from {DATA_FILE}")
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Loaded data: {data}")
            for name in VALID_NAMES:
                if name not in data:
                    data[name] = 0.0
            return data
    except Exception as e:
        print(f"Error loading data: {e}")
        traceback.print_exc()
        return {name: 0.0 for name in VALID_NAMES}


def save_data(data):
    print("Entering save_data")
    try:
        print(f"Saving data to {DATA_FILE}: {data}")
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved successfully to {DATA_FILE}")
        # Проверка сохраненных данных
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
            print(f"Verified saved data: {saved_data}")
    except Exception as e:
        print(f"Error saving data: {e}")
        traceback.print_exc()


@app.route("/", methods=["GET", "POST"])
def index():
    print("Entering index route")
    try:
        data = load_data()
        print(f"Processing request, data: {data}")
        if request.method == "POST":
            print("Handling POST request")
            name = request.form["name"]
            try:
                km = float(request.form["km"])
                if name in VALID_NAMES:
                    data[name] = data.get(name, 0.0) + km
                    save_data(data)
            except ValueError as e:
                print(f"Invalid input for km: {e}")
            return redirect("/")

        sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
        max_km = 100
        print(f"Rendering template with sorted_data: {sorted_data}, max_km: {max_km}")
        return render_template("index.html", data=sorted_data, max_km=max_km, valid_names=VALID_NAMES)
    except Exception as e:
        print(f"Error in index route: {e}")
        traceback.print_exc()
        return "Internal Server Error", 500


if __name__ == "__main__":
    print("Starting Flask app locally")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)