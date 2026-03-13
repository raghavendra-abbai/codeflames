from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = "database/db.sqlite3"
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():

    if not os.path.exists("database"):
        os.makedirs("database")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    conn = sqlite3.connect(DATABASE)

    # Farmers table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS farmers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        password TEXT
    )
    """)

    # Consumers table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS consumers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        password TEXT
    )
    """)


    # Crops table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS crops(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT,
        price REAL,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# FARMER REGISTER
# -----------------------------
@app.route("/farmer_register", methods=["GET","POST"])
def farmer_register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            "INSERT INTO farmers (name,email,mobile,password) VALUES (?,?,?,?)",
            (name,email,mobile,password)
        )

        conn.commit()
        conn.close()

        return redirect("/farmer_login")

    return render_template("farmer_register.html")


# -----------------------------
# FARMER LOGIN
# -----------------------------
@app.route("/farmer_login", methods=["GET","POST"])
def farmer_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        farmer = conn.execute(
            "SELECT * FROM farmers WHERE email=? AND password=?",
            (email,password)
        ).fetchone()

        conn.close()

        if farmer:
            return redirect("/farmer_dashboard")

    return render_template("farmer_login.html")


@app.route("/farmer_dashboard")
def farmer_dashboard():

    conn = get_db()

    crops = conn.execute(
        "SELECT * FROM crops WHERE farmer_id=1"
    ).fetchall()

    conn.close()

    return render_template("farmer_dashboard.html", crops=crops)


# -----------------------------
# ADD CROP (Farmer)
# -----------------------------
@app.route("/add_crop", methods=["GET","POST"])
def add_crop():

    if request.method == "POST":

        crop_name = request.form["crop_name"]
        price = request.form["price"]

        image = request.files["image"]

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)

        conn = get_db()

        conn.execute(
            "INSERT INTO crops (farmer_id,crop_name,price,image) VALUES (?,?,?,?)",
            (1, crop_name, price, image.filename)
        )

        conn.commit()
        conn.close()

        return redirect("/farmer_dashboard")

    return render_template("add_crop.html")
# -----------------------------
# CONSUMER REGISTER
# -----------------------------
@app.route("/consumer_register", methods=["GET","POST"])
def consumer_register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            "INSERT INTO consumers (name,email,mobile,password) VALUES (?,?,?,?)",
            (name,email,mobile,password)
        )

        conn.commit()
        conn.close()

        return redirect("/consumer_login")

    return render_template("consumer_register.html")


# -----------------------------
# CONSUMER LOGIN
# -----------------------------
@app.route("/consumer_login", methods=["GET","POST"])
def consumer_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        consumer = conn.execute(
            "SELECT * FROM consumers WHERE email=? AND password=?",
            (email,password)
        ).fetchone()

        conn.close()

        if consumer:
            return redirect("/consumer_dashboard")

    return render_template("consumer_login.html")


@app.route("/consumer_dashboard")
def consumer_dashboard():
    return render_template("consumer_dashboard.html")


# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/admin_dashboard")

    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/view_crops")
def view_crops():

    conn = get_db()

    crops = conn.execute(
        "SELECT * FROM crops"
    ).fetchall()

    conn.close()

    return render_template("view_crops.html", crops=crops)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":

    init_db()

    app.run(debug=True)