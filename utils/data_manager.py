import json
import os

DATABASE_FOLDER = "database"
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "project_data.json")


def initialize_database():
    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as file:
            json.dump({
                "project": {},
                "geometry": {},
                "welding": {},
                "distortion": {}
            }, file, indent=4)


def load_data():
    initialize_database()

    with open(DATABASE_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def save_section(section, values):
    data = load_data()
    data[section] = values
    save_data(data)


def load_section(section):
    data = load_data()
    return data.get(section, {})