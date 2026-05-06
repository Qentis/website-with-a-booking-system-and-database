from flask import Flask, render_template, request, redirect
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import os

from db import (
    SessionLocal,
    Unit,
    Property,
    Guest,
    add_property,
    add_guest,
    add_booking,
    add_unit
)

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


from sqlalchemy.orm import joinedload

@app.route("/")
def index():
    with SessionLocal() as session:
        units = session.query(Unit)\
            .options(
                joinedload(Unit.property),
                joinedload(Unit.bookings)  
            )\
            .all()

    return render_template("index.html", units=units)

@app.route("/book/<int:unit_id>", methods=["GET", "POST"])
def book(unit_id):

    if request.method == "POST":

        name = request.form["name"]
        surname = request.form["surname"]
        contact = request.form["contact"]

        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        guest = add_guest(name, surname, contact)

        if guest is None:
            return "Ошибка создания гостя"

        add_booking(
            guest_id=guest.id,
            unit_id=unit_id,
            check_in=check_in,
            check_out=check_out
        )

        return redirect("/")

    return render_template("booking.html", unit_id=unit_id)


@app.route("/add_property", methods=["GET", "POST"])
def add_property_page():

    if request.method == "POST":

        name = request.form["name"]
        address = request.form["address"]
        description = request.form["description"]

        type_ = request.form.get("type")

        unit_title = request.form.get("unit_title")
        capacity = request.form.get("capacity")
        price = request.form.get("price")

        file = request.files.get("image")

        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        prop = add_property(name, address, description, filename)

        if prop is None:
            return "Ошибка создания объекта"
        
        if type_ == "apartment":
            add_unit(prop.id, "Апартаменты", 2, 50)

        elif unit_title and capacity and price:
            add_unit(prop.id, unit_title, int(capacity), float(price))

        add_unit(
            prop.id,
            unit_title or "Standard",
            int(capacity) if capacity else 2,
            float(price) if price else 50
        )

        return redirect("/")

    return render_template("add_property.html")


if __name__ == "__main__":
    app.run(debug=True)