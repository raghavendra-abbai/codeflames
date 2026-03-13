from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

DATABASE = "database/db.sqlite3"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/farmer", methods=["GET","POST"])
def farmer():
    if request.method == "POST":
        name = request.form["name"]
        crop = request.form["crop"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        conn = get_db()
        conn.execute(
            "INSERT INTO products (farmer,crop,quantity,price,date) VALUES (?,?,?,?,?)",
            (name,crop,quantity,price,str(datetime.datetime.now()))
        )
        conn.commit()

        return redirect("/dashboard")

    return render_template("farmer.html")

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    return render_template("dashboard.html", products=products)

@app.route("/track", methods=["GET","POST"])
def track():
    product=None
    if request.method=="POST":
        pid=request.form["product_id"]
        conn=get_db()
        product=conn.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()

    return render_template("track_product.html",product=product)

if __name__ == "__main__":
    app.run(debug=True)