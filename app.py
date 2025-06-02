from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# Список допустимых имен
VALID_NAMES = ["Виктор", "Эми", "Леша"]

# Путь к файлу данных
DATA_FILE = os.environ.get("DATA_FILE", "/data/data.json")


def ensure_data_file():
    """Проверяет и создает директорию и файл data.json, если они не существуют."""
    data_dir = os.path.dirname(DATA_FILE)
    try:
        # Создаем директорию, если она не существует
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created directory: {data_dir}")

        # Создаем файл data.json с начальными данными, если он не существует
        if not os.path.exists(DATA_FILE):
            initial_data = {name: 0.0 for name in VALID_NAMES}
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            print(f"Created initial data file: {DATA_FILE}")
    except Exception as e:
        print(f"Error initializing data file: {e}")


def load_data():
    try:
        ensure_data_file()  # Убедимся, что файл и директория существуют
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all valid names have an entry, defaulting to 0
            for name in VALID_NAMES:
                if name not in data:
                    data[name] = 0.0
            return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return {name: 0.0 for name in VALID_NAMES}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved successfully to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving data: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    if request.method == "POST":
        name = request.form["name"]
        try:
            km = float(request.form["km"])
            if name in VALID_NAMES:  # Only process if name is valid
                data[name] = data.get(name, 0.0) + km
                save_data(data)
        except ValueError as e:
            print(f"Invalid input for km: {e}")
        return redirect("/")

    # Sort by kilometers and find max for percentage with safe fallback
    sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
    values = list(sorted_data.values())
    max_km = max(values) if values and max(values) > 0 else 1  # Fallback to 1 if all values are 0 or empty
    return render_template("index.html", data=sorted_data, max_km=max_km, valid_names=VALID_NAMES)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)