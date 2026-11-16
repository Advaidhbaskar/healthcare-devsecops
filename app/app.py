
import os
import re
from datetime import date

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Demo application only. Never use real patient information.
appointments = []

DEPARTMENTS = {
    "Cardiology",
    "Neurology",
    "General Medicine",
    "Orthopedics",
    "Dermatology"
}


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; "
        "form-action 'self'; frame-ancestors 'none'"
    )
    return response


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", appointments=appointments)


@app.route("/book", methods=["POST"])
def book_appointment():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()
    appointment_date = request.form.get("date", "").strip()

    if not name or len(name) > 60:
        return jsonify({"error": "Invalid name"}), 400

    if not re.fullmatch(r"[A-Za-z ]+", name):
        return jsonify({"error": "Name must contain letters only"}), 400

    if department not in DEPARTMENTS:
        return jsonify({"error": "Invalid department"}), 400

    try:
        selected_date = date.fromisoformat(appointment_date)
        if selected_date < date.today():
            return jsonify({"error": "Date cannot be in the past"}), 400
    except ValueError:
        return jsonify({"error": "Invalid appointment date"}), 400

    appointment = {
        "name": name,
        "department": department,
        "date": appointment_date
    }

    appointments.append(appointment)

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment": appointment
    }), 201


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "Healthcare Appointment System"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
