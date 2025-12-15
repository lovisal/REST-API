from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO students (id, name, marks) VALUES (?, ?, ?)",
        (data["id"], data["name"], data["marks"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added"})

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE students SET name=?, marks=? WHERE id=?",
        (data["name"], data["marks"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(debug=True)
