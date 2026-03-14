from flask import Flask, render_template, request, redirect
import sqlite3
import os
from PIL import Image
from PIL.ExifTags import TAGS

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

    # Farmers
    conn.execute("""
    CREATE TABLE IF NOT EXISTS farmers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        password TEXT
    )
    """)

    # Consumers
    conn.execute("""
    CREATE TABLE IF NOT EXISTS consumers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        password TEXT
    )
    """)

    # Crops
    conn.execute("""
    CREATE TABLE IF NOT EXISTS crops(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT,
        price REAL,
        image TEXT,
        status TEXT
    )
    """)

    # Orders
    conn.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_id INTEGER,
        crop_name TEXT,
        price REAL,
        quantity INTEGER,
        customer_name TEXT,
        mobile TEXT,
        address TEXT
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
# Check GeoTag
# -----------------------------
def has_geotag(image_path):

    try:

        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return False

        for tag_id in exif_data:

            tag = TAGS.get(tag_id, tag_id)

            if tag == "GPSInfo":
                return True

        return False

    except:
        return False


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# Farmer Register
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
# Farmer Login
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


# -----------------------------
# Farmer Dashboard
# -----------------------------
@app.route("/farmer_dashboard")
def farmer_dashboard():

    conn = get_db()

    crops = conn.execute("SELECT * FROM crops").fetchall()

    conn.close()

    return render_template("farmer_dashboard.html", crops=crops)


# -----------------------------
# Add Crop
# -----------------------------
@app.route("/add_crop", methods=["GET","POST"])
def add_crop():

    if request.method == "POST":

        crop_name = request.form["crop_name"]
        price = request.form["price"]

        image = request.files["image"]

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)

        if not has_geotag(image_path):

            os.remove(image_path)

            return "<script>alert('Upload geotagged image only');window.history.back();</script>"

        conn = get_db()

        conn.execute(
            "INSERT INTO crops (crop_name,price,image,status) VALUES (?,?,?,?)",
            (crop_name,price,image.filename,"pending")
        )

        conn.commit()
        conn.close()

        return redirect("/farmer_dashboard")

    return render_template("add_crop.html")


# -----------------------------
# Admin Login
# -----------------------------
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/admin_dashboard")

    return render_template("admin_login.html")


# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


# -----------------------------
# View Farmer Crops
# -----------------------------
@app.route("/view_farmer_crops")
def view_farmer_crops():

    conn = get_db()

    crops = conn.execute("SELECT * FROM crops").fetchall()

    conn.close()

    return render_template("admin_crop.html", crops=crops, mode="view")


# -----------------------------
# Approve / Publish Crops
# -----------------------------
@app.route("/admin_crop")
def admin_crop():

    conn = get_db()

    crops = conn.execute("SELECT * FROM crops").fetchall()

    conn.close()

    return render_template("admin_crop.html", crops=crops, mode="action")


# -----------------------------
# Approve Crop
# -----------------------------
@app.route("/approve_crop/<int:id>")
def approve_crop(id):

    conn = get_db()

    conn.execute(
        "UPDATE crops SET status='approved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin_crop")


# -----------------------------
# Reject Crop
# -----------------------------
@app.route("/reject_crop/<int:id>")
def reject_crop(id):

    conn = get_db()

    conn.execute(
        "UPDATE crops SET status='rejected' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin_crop")


# -----------------------------
# Publish Crop
# -----------------------------
@app.route("/publish_crop/<int:id>")
def publish_crop(id):

    conn = get_db()

    conn.execute(
        "UPDATE crops SET status='published' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin_crop")


# -----------------------------
# Consumer Register
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
# Consumer Login
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


# -----------------------------
# Consumer Dashboard
# -----------------------------
@app.route("/consumer_dashboard")
def consumer_dashboard():

    search = request.args.get("search")

    conn = get_db()

    if search:
        crops = conn.execute(
            "SELECT * FROM crops WHERE status='published' AND crop_name LIKE ?",
            ('%' + search + '%',)
        ).fetchall()
    else:
        crops = conn.execute(
            "SELECT * FROM crops WHERE status='published'"
        ).fetchall()

    conn.close()

    return render_template("consumer_dashboard.html", crops=crops)


# -----------------------------
# Buy Crop
# -----------------------------
@app.route("/buy_crop/<int:id>", methods=["GET","POST"])
def buy_crop(id):

    conn = get_db()

    crop = conn.execute(
        "SELECT * FROM crops WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        quantity = request.form["quantity"]
        address = request.form["address"]

        conn.execute(
            "INSERT INTO orders (crop_id,crop_name,price,quantity,customer_name,mobile,address) VALUES (?,?,?,?,?,?,?)",
            (crop["id"], crop["crop_name"], crop["price"], quantity, name, mobile, address)
        )

        conn.commit()
        conn.close()

        return """
        <script>
        alert("Order placed successfully!");
        window.location="/consumer_dashboard";
        </script>
        """

    return render_template("buy_crop.html", crop=crop)

# -----------------------------
# ADMIN VIEW ORDERS
# -----------------------------
@app.route("/admin_orders")
def admin_orders():

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders"
    ).fetchall()

    conn.close()

    return render_template("admin_orders.html", orders=orders)
@app.route("/user_portal")
def user_portal():
    return render_template("user_portal.html")


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":

    init_db()
    app.run(debug=True)