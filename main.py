from flask import Flask, request, jsonify, Response
import uuid
import json
import os
import jwt
import datetime
from utils import bookings_to_xml, validate_xml
from flask import render_template
from flask import request, redirect
import webbrowser
import threading

app = Flask(__name__)

SECRET_KEY = "cheie_secreta"
DATA_FILE = "data.json"

#incarca rezervarile din fisierul json daca acesta exista
def load_bookings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# salveaza rezervarile curente in fisierul json
def save_bookings():
    with open(DATA_FILE, "w") as f:
        json.dump(bookings, f, indent=2)

# variabila globala care contine toate rezervarile
bookings = load_bookings()

# genereaza un JWT valid pentru o ora
def generate_token(username):
    payload = {
        "user": username,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# verifica validitatea unui token JWT
def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("user") == "admin"
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

# extrage token-ul din headerul HTTP si verifica autentificarea
def require_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return False
    try:
        token = auth_header.split(" ")[1]
        return verify_token(token)
    except Exception:
        return False

# endpoint pentru login; primeste username si parola si returneaza tokenul JWT daca sunt corecte
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        token = generate_token(username)
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

# redirectioneaza accesul de la root catre dashboardul vizual
@app.route("/")
def index():
    return redirect("/dashboard")

# returneaza toate rezervarile sau rezervarile filtrate dupa nume, camera sau data
@app.route("/bookings", methods=["GET"])
def get_bookings():
    name = request.args.get("name")
    room = request.args.get("room")
    date = request.args.get("date")

    filtered = bookings
    if name:
        filtered = [b for b in filtered if b["name"].lower() == name.lower()]
    if room:
        filtered = [b for b in filtered if b["room"] == room]
    if date:
        filtered = [b for b in filtered if b["date"] == date]

    return jsonify(filtered)

# creeaza o rezervare noua (daca tokenul este valid)
@app.route("/bookings", methods=["POST"])
def create_booking():
    if not require_token(request):
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    new_booking = {
        "id": str(uuid.uuid4()),
        "name": data.get("name"),
        "room": data.get("room"),
        "date": data.get("date")
    }
    bookings.append(new_booking)
    save_bookings()
    return jsonify(new_booking), 201

# sterge o rezervare dupa ID (daca tokenul este valid)
@app.route("/bookings/<booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    if not require_token(request):
        return jsonify({"message": "Unauthorized"}), 401

    global bookings
    bookings = [b for b in bookings if b["id"] != booking_id]
    save_bookings()
    return jsonify({"message": "Booking deleted."}), 200

# exporta rezervarile in format XML (folosind functia din utils)
@app.route("/bookings/xml", methods=["GET"])
def export_bookings_xml():
    xml_string = bookings_to_xml(bookings)
    return Response(xml_string, mimetype="application/xml")

# valideaza XMl-ul generat cu un XSD
@app.route("/bookings/validate", methods=["GET"])
def validate_bookings_xml():
    success, message = validate_xml()
    status = 200 if success else 400
    return jsonify({"valid": success, "message": message}), status

# interfata vizuala principala : afisare rezervari + adaugare + filtrare + validare
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global bookings
    validation_result = None

    # form submit pentru rezervare noua
    if request.method == "POST":
        data = request.form
        new_booking = {
            "id": str(uuid.uuid4()),
            "name": data.get("name"),
            "room": data.get("room"),
            "date": data.get("date")
        }
        bookings.append(new_booking)
        save_bookings()
        return redirect("/dashboard")

    # filtrare + validare XML la GET
    name = request.args.get("name")
    room = request.args.get("room")
    date = request.args.get("date")
    validate = request.args.get("validate")

    filtered = bookings
    if name:
        filtered = [b for b in filtered if b["name"].lower() == name.lower()]
    if room:
        filtered = [b for b in filtered if b["room"] == room]
    if date:
        filtered = [b for b in filtered if b["date"] == date]

    if validate == "true":
        success, message = validate_xml()
        validation_result = {
            "valid": success,
            "message": message
        }
    return render_template("dashboard.html", bookings=filtered, validation=validation_result)

# endpoint pentru stergerea rezervarilor din dashboard
@app.route("/delete/<booking_id>", methods=["POST"])
def delete_booking_ui(booking_id):
    global bookings
    bookings = [b for b in bookings if b["id"] != booking_id]
    save_bookings()
    return redirect("/dashboard")

# deshide automat dashboard-ul in browser la pornire
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# pornire aplicatie + browser
if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
