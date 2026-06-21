import os
from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "name": "Anshika", "course": "IT Engineering"},
    {"id": 2, "name": "Rahul", "course": "CSE"}
]

REQUIRED_FIELDS = {"name", "course"}


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    new_student = {
        "id": max((s["id"] for s in students), default=0) + 1,
        "name": data["name"],
        "course": data["course"],
    }
    students.append(new_student)
    return jsonify(new_student), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    if "name" in data:
        student["name"] = data["name"]
    if "course" in data:
        student["course"] = data["course"]
    return jsonify(student)


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    original_count = len(students)
    students = [s for s in students if s["id"] != student_id]
    if len(students) == original_count:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted"})


if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
