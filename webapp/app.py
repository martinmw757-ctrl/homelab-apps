from flask import Flask, request, redirect
import psycopg2, os

app = Flask(__name__)

DB = {
    "host": os.environ["DB_HOST"],        # the doorbell's NAME — apps never use IPs
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            conn = psycopg2.connect(**DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO visitors (name) VALUES (%s)", (name,))
            conn.commit()
            cur.close(); conn.close()
        return redirect("/")

    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("SELECT name, visited_at FROM visitors ORDER BY visited_at DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close(); conn.close()

    items = "".join(f"<li>{r[0]} — {r[1].strftime('%H:%M:%S')}</li>" for r in rows)
    return f"""<h1>Homelab Visitors</h1>
    <form method="post"><input name="name" placeholder="your name">
    <button>Add</button></form>
    <ul>{items}</ul>"""
